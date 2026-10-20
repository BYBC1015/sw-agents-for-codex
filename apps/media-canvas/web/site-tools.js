/* Optional WebMCP bridge. Conversation writes always name the project and binding. */
(async()=>{
 const status=document.getElementById('site-tools-status');
 if(typeof document.modelContext?.registerTool!=='function'){status.textContent='网页工具未启用 · 可使用 CLI';return;}
 const schema=(properties,required=[])=>({type:'object',properties,required,additionalProperties:false});
 const str={type:'string'},pid={type:'string',description:'目标项目的真实编号；不从浏览器切换推断。'},cid={type:'string',description:'当前实际 Codex 对话编号，可读取 CODEX_THREAD_ID；不能编造。'};
 const offset={type:'integer',minimum:0,default:0},limit={type:'integer',minimum:1,maximum:20,default:3};
 const task={type:'string',description:'项目内任务编号，如 T001。'};
 const scope={projectId:pid,conversationId:cid,bindingVersion:{type:'integer',minimum:1}};
 const file=schema({path:str,title:str,mode:{type:'string',enum:['reference','copy'],default:'reference'},parentNode:str},['path']);
 const files={type:'array',items:file,maxItems:30};
 const nodes={type:'array',items:str,maxItems:100};
 function ready(){if(!state)throw new Error('画布尚未加载');}
 function sameProject(args){ready();if(args.projectId&&args.projectId!==state.projectId)throw new Error('当前页面显示其他项目，请先打开目标项目');}
 const tool=(name,description,inputSchema,execute,readOnly=true)=>({name,description,inputSchema,annotations:{readOnlyHint:readOnly},execute:async args=>{await canvasReady;return execute(args);}});
 const write=async(path,args)=>{sameProject(args);await ensureSaved();const result=await api(path,args);await load(true);return result;};
 const definitions=[
  tool('get_canvas_storyboard','按需分页读取镜头或公共资产；不包含图片。',schema({projectId:pid,kind:{type:'string',enum:['shots','entities']},offset,limit},['projectId']),a=>{sameProject(a);return api('/api/storyboard?'+new URLSearchParams({kind:a.kind||'shots',offset:a.offset||0,limit:a.limit||3}));}),
  tool('get_canvas_shot_packet','读取指定镜头选定版本、固定引用与生成锁定项。',schema({projectId:pid,shotId:str},['projectId','shotId']),a=>{sameProject(a);return api('/api/shot-packet?shot='+encodeURIComponent(a.shotId));}),
  tool('get_canvas_entity_impact','修改公共资产前，读取受影响镜头；不会修改或生成。',schema({projectId:pid,entityId:str},['projectId','entityId']),a=>{sameProject(a);return api('/api/storyboard-impact?entity='+encodeURIComponent(a.entityId));}),
  tool('export_canvas_storyboard','导出当前选定镜头清单；final 要求无缺图、依赖变化或未通过验收。',schema({projectId:pid,final:{type:'boolean'}},['projectId']),a=>{sameProject(a);return api('/api/storyboard-export?final='+(a.final?'1':'0'));}),
  tool('edit_canvas_storyboard','保存版本化镜头/实体、切换历史版本或记录已完成的视觉验收；不生成媒体。重试原 requestId。',schema({...scope,requestId:str,expectedRevision:{type:'integer'},action:{type:'string',enum:['entity','shot','select','review']},id:str,kind:str,version:{type:'integer'},shotVersion:{type:'integer'},status:{type:'string',enum:['pass','fail']},evidence:str,fields:schema({title:str,description:str,script:str,camera:str,duration:{type:'number'},locks:{type:'array',items:str},assetId:{type:['string','null']},outputAssetId:{type:['string','null']},entityRefs:{type:'object',additionalProperties:{type:'integer'}}})},['projectId','conversationId','bindingVersion','requestId','expectedRevision','action','id']),a=>write('/api/storyboard',a),false),
  tool('get_canvas_projects','仅在选择或接续项目时搜索。',schema({query:str,offset,limit}),a=>api('/api/projects?'+new URLSearchParams({q:a.query||'',offset:a.offset||0,limit:a.limit||3}))),
  tool('open_canvas_project','打开指定项目；保留原对话绑定，浏览不等于切换执行目标。',schema({projectId:pid},['projectId']),async a=>{await switchProject(a.projectId);return {projectId:a.projectId,opened:true};},false),
  tool('get_canvas_binding','读取实际对话的持久项目绑定。',schema({conversationId:cid},['conversationId']),a=>api('/api/binding?conversation='+encodeURIComponent(a.conversationId))),
  tool('bind_canvas_conversation','用户要求切换或接续项目时，将当前真实对话绑定到本页项目；不会执行任务。先读绑定版本。',schema({...scope,expectedVersion:{type:'integer',minimum:0},label:str},['projectId','conversationId','expectedVersion']),async a=>{
   sameProject(a);await ensureSaved();if(projectBusy||submitting)throw new Error('请等当前操作完成');const result=await api('/api/bind',a);conversationId=a.conversationId;history.replaceState(null,'',projectUrl(routedProject));await refreshBinding();return result;
  },false),
  tool('get_canvas_context','默认短摘要；since 传上次 cursor，未变化只回状态。选区用 scope=selection，任务用 task。',schema({projectId:pid,task,scope:{type:'string',enum:['overview','selection']},since:str,offset,limit}),a=>{
   if(!state){if(a.projectId)throw new Error('尚未打开目标项目');return {mode:'blank',projectId:null};}sameProject(a);
   if(!a.task&&a.scope!=='selection')return api('/api/summary?'+new URLSearchParams(a.since?{since:a.since}:{}));
   return api('/api/read-context',{projectId:state.projectId,task:a.task,nodeIds:Array.from(selected),offset:a.offset||0,limit:a.limit||3});}),
  tool('get_canvas_detail','按需展开。kind=project 读完整交接（支持 section/checkpoint）；kind=handoff 取接续指令。',schema({projectId:pid,task,kind:{type:'string',enum:['assets','annotations','notes','result','project','handoff']},section:{type:'string',enum:['summary','assets','nodes','edges','annotations','notes','tasks','versions','shots','entities']},checkpoint:str,offset,limit},['kind']),a=>{
   sameProject(a);const q=new URLSearchParams({offset:a.offset||0,limit:a.limit||3});if(a.task)q.set('task',a.task);
   if(a.checkpoint)q.set('checkpoint',a.checkpoint);
   if(a.kind==='project'){q.set('section',a.section||'summary');return api('/api/project-handoff?'+q);}
   if(a.kind==='handoff')return api('/api/handoff?'+q);
   q.set('kind',a.kind);if(!a.task)q.set('nodes',Array.from(selected).join(','));return api('/api/detail?'+q);}),
  tool('create_canvas_project','仅在用户要新建时创建空项目并绑定实际对话；不执行任务。',schema({conversationId:cid,requestId:str,name:str,goal:str},['conversationId','requestId','name']),async a=>{
   await ensureSaved();const current=await api('/api/binding?conversation='+encodeURIComponent(a.conversationId));
   const p=await api('/api/projects/new',{requestId:a.requestId,name:a.name,goal:a.goal||''});
   await api('/api/bind',{conversationId:a.conversationId,projectId:p.projectId,expectedVersion:current.version,label:'当前对话'});
   conversationId=a.conversationId;await switchProject(p.projectId);return {projectId:p.projectId,created:true};},false),
  tool('locate_canvas_node','定位已有节点；只改变页面选区和视图。',schema({projectId:pid,nodeId:str},['projectId','nodeId']),async a=>{sameProject(a);if(!state.nodes.some(n=>n.id===a.nodeId))throw new Error('节点不存在');await ensureSaved();centerNode(a.nodeId);await ensureSaved();return {nodeId:a.nodeId,located:true};},false),
  tool('add_canvas_note','保存用户要求记录的方案或结论，重试复用 requestId。',schema({...scope,requestId:str,title:str,text:str,nodeIds:nodes},['projectId','conversationId','requestId','title','text']),a=>write('/api/notes',a),false),
  tool('import_canvas_assets','将用户指定素材加入已绑定项目；reference 引用原件，copy 复制到过程/导入素材。重试复用 requestId。',schema({...scope,requestId:str,files},['projectId','conversationId','requestId','files']),a=>write('/api/ingest',a),false),
  tool('create_canvas_task','保存固定输入任务；discuss 只讨论，execute 也不会自动运行。',schema({...scope,requestId:str,intent:{type:'string',enum:['discuss','execute']},text:str,nodeIds:nodes,frameRange:str},['projectId','conversationId','requestId','intent','text','nodeIds']),a=>write('/api/tasks',a),false),
  tool('claim_canvas_task','仅在用户要求处理指定任务时认领；不运行媒体工具。',schema({...scope,task},['projectId','conversationId','task']),a=>write('/api/claim',a),false),
  tool('write_canvas_result','将已完成任务的输出文件、版本关系和结果说明原子回写为待确认；不会生成媒体。重试复用 requestId。',schema({...scope,requestId:str,task,text:str,files},['projectId','conversationId','requestId','task','text']),a=>write('/api/result',a),false),
  tool('update_canvas_project','记录已确认目标、决定、下一步及项目进度；不把假设写成确认。',schema({...scope,expectedRevision:{type:'integer'},name:str,goal:str,decisions:str,nextStep:str,constraints:{type:'array',items:str,maxItems:20},progress:schema({stage:str,blockers:str,openQuestions:str,deliveryNotes:str})},['projectId','conversationId','expectedRevision']),a=>write('/api/project',a),false),
  tool('save_canvas_checkpoint','保存整个项目的不可变交接快照，包含所有文字和素材引用，不复制媒体。',schema({...scope,expectedRevision:{type:'integer'},requestId:str,title:str},['projectId','conversationId','expectedRevision','requestId','title']),a=>write('/api/checkpoints',a),false)
 ];
 const basic=new Set(['get_canvas_projects','get_canvas_binding','get_canvas_context','get_canvas_detail']);
 const registered=new Set();let expanding=null;
 async function register(definition){if(registered.has(definition.name))return;await document.modelContext.registerTool(definition);registered.add(definition.name);}
 async function expand(){if(!expanding)expanding=(async()=>{for(const d of definitions)await register(d);status.textContent='完整对话工具已就绪';return {enabled:true,tools:registered.size};})().finally(()=>{expanding=null;});return expanding;}
 try{for(const definition of definitions.filter(d=>basic.has(d.name)))await register(definition);
 await register(tool('enable_canvas_actions','需要创建、打开、绑定或写入时调用一次，按需加载操作工具。',schema({}),expand));
 status.textContent='轻量对话模式 · 操作工具按需加载';}catch(e){status.textContent='工具连接未完成 · 可使用 CLI';console.warn(e.message);}
})();
