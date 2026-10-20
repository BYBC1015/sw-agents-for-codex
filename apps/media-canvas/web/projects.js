/* Project browsing is separate from conversation binding. All writes retain their project. */
let bindingState=null,projectListOffset=0,projectQueryToken=0,versionEdit=null,checkpointRequest=null;
function projectUrl(pid,conversation=conversationId){const url=new URL(location.href);url.searchParams.set('project',pid);if(conversation)url.searchParams.set('conversation',conversation);else url.searchParams.delete('conversation');return url;}
async function switchProject(pid,bind=false){
 await ensureSaved();if(projectBusy||submitting)throw new Error('当前操作尚未结束，完成后即可切换项目。');
 saveComposer();if(bind&&conversationId){const current=await api('/api/binding?conversation='+encodeURIComponent(conversationId));await api('/api/bind',{projectId:pid,conversationId,expectedVersion:current.version,label:'当前对话'});}
 await api('/api/projects/open',{projectId:pid});const url=projectUrl(pid);url.searchParams.delete('projects');location.assign(url);
}
async function refreshBinding(){
 if(!conversationId){$('#binding-status').textContent='对话未绑定 · 在聊天中说“绑定这个画布”';return;}
 bindingState=await api('/api/binding?conversation='+encodeURIComponent(conversationId));
 const match=bindingState.projectId===routedProject;
 $('#binding-status').textContent=bindingState.projectId?(match?'对话已绑定：':'正在浏览其他项目 · 对话仍绑定：')+(bindingState.label||'当前对话')+' / '+bindingState.projectName:'此对话尚未绑定项目';
 $('.binding-bar').classList.toggle('mismatch',!!bindingState.projectId&&!match);
 $('#binding-follow').hidden=!bindingState.projectId||match;
 $('#binding-copy').textContent=match?'复制对话接续指令':'让对话绑定此项目';
}
$('#binding-follow').onclick=()=>switchProject(bindingState.projectId).catch(e=>toast(e.message));
$('#binding-copy').onclick=async()=>{
 try{if(conversationId&&bindingState?.projectId!==routedProject){await ensureSaved();const current=await api('/api/binding?conversation='+encodeURIComponent(conversationId));await api('/api/bind',{projectId:routedProject,conversationId,expectedVersion:current.version,label:'当前对话'});await refreshBinding();return;}
 const h=await api('/api/handoff');$('#handoff-text').value='使用 SW Canvas，将当前真实 Codex 对话绑定到此项目，再读取完整项目摘要。仅绑定和读取，不执行媒体任务。\n'+h.text;$('#handoff-dialog').showModal();}catch(e){toast(e.message);}
};
async function listProjects(append=false){
 const token=++projectQueryToken,query=$('#projects-search').value.trim();if(!append)projectListOffset=0;
 const result=await api('/api/projects?'+new URLSearchParams({q:query,offset:projectListOffset,limit:12}));if(token!==projectQueryToken)return;
 const box=$('#projects-list');if(!append)box.replaceChildren();
 if(!result.total)box.append(el('p','empty','没有匹配的项目，可以新建一个。'));
 for(const p of result.items){const row=el('section','project-row');const info=el('div');info.append(el('strong','',p.name),el('small','',p.projectId+(p.unavailable?' · 文件离线':` · ${p.assetCount} 项素材 · ${p.activeTasks} 项待办`)));if(p.goal)info.append(el('p','',p.goal));row.append(info);
  const button=el('button',p.projectId===routedProject?'':'primary',p.projectId===routedProject?'当前项目':(!routedProject&&conversationId?'打开并绑定此对话':'打开'));button.disabled=!!p.unavailable||p.projectId===routedProject;button.onclick=()=>switchProject(p.projectId,!routedProject).catch(e=>toast(e.message));row.append(button);box.append(row);}
 projectListOffset=result.nextOffset;$('#projects-more').hidden=result.nextOffset===null;
}
function openProjects(create=false){$('#projects-heading').textContent=create?'新建画布':'选择已有项目';$('#projects-create').open=create;for(const node of [$('#projects-search'),$('label[for="projects-search"]'),$('#projects-list')])node.hidden=create;$('#projects-more').hidden=true;$('#projects-dialog').showModal();if(!create)listProjects().catch(e=>toast(e.message));else $('#new-project-name').focus();}
$('#projects-open').onclick=()=>openProjects();
$('#blank-new').onclick=()=>openProjects(true);$('#blank-existing').onclick=()=>openProjects();
let projectSearchTimer;$('#projects-search').oninput=()=>{clearTimeout(projectSearchTimer);projectSearchTimer=setTimeout(()=>listProjects().catch(e=>toast(e.message)),180);};
$('#projects-more').onclick=()=>listProjects(true).catch(e=>toast(e.message));
$('#new-project-form').onsubmit=async event=>{
 event.preventDefault();const button=$('#new-project-submit');button.disabled=true;
 try{await ensureSaved();if(projectBusy||submitting)throw new Error('请等待当前操作完成');
  const data={name:$('#new-project-name').value.trim(),goal:$('#new-project-goal').value.trim()},key='sw-canvas-new-project';let saved=JSON.parse(localStorage.getItem(key)||'null');
  if(!saved||JSON.stringify(saved.data)!==JSON.stringify(data)){saved={data,requestId:crypto.randomUUID()};localStorage.setItem(key,JSON.stringify(saved));}
  const result=await api('/api/projects/new',{...data,requestId:saved.requestId});await switchProject(result.projectId,true);localStorage.removeItem(key);
 }catch(e){toast(e.message);}finally{button.disabled=false;}
};
function addHandoffSection(box,title,value){box.append(el('h3','',title),el('p','handoff-value',value||'尚未记录'));}
async function openProjectHandoff(){
 await ensureSaved();const result=await api('/api/project-handoff'),box=$('#project-handoff-content');box.replaceChildren();
 box.append(el('p','',result.project.name+' · '+result.project.projectId+' · 修订 '+result.revision));
 addHandoffSection(box,'目标与当前阶段',result.project.goal+'\n'+(result.progress.stage||''));
 addHandoffSection(box,'已确认决定',result.project.decisions);addHandoffSection(box,'约束',result.project.constraints.join('\n'));
 addHandoffSection(box,'下一步',result.project.nextStep);addHandoffSection(box,'阻塞与待确认问题',[result.progress.blockers,result.progress.openQuestions].filter(Boolean).join('\n'));
 addHandoffSection(box,'版本取舍',result.versionChoices.items.map(v=>`${({candidate:'候选',selected:'已选定',rejected:'未采用',delivered:'已交付'}[v.disposition])} · ${v.title}：${v.reason||'未填写原因'}`).join('\n')+(result.versionChoices.nextOffset!==null?'\n更多取舍保存在完整交接中。':''));
 addHandoffSection(box,'任务进度',Object.entries(result.taskCounts).map(([key,value])=>statuses[key]+' '+value).join(' · '));
 addHandoffSection(box,'交付要求',result.progress.deliveryNotes);addHandoffSection(box,'文件位置','过程：'+result.paths.process+'\n交付：'+result.paths.delivery);
 box.append(el('p','small muted',`${result.counts.assets} 项素材、${result.counts.notes} 条方案、${result.counts.annotations} 条标注、${result.counts.edges} 条关系均保存在快照中。快照不复制媒体文件。`));
 $('#project-handoff-dialog').showModal();await renderCheckpoints();
}
async function renderCheckpoints(){const list=$('#checkpoint-list');list.replaceChildren();const result=await api('/api/checkpoints');if(result.total)list.append(el('h3','','最近的交接快照'));
 for(const item of result.items){const button=el('button','full',item.title+' · 修订 '+item.revision);button.onclick=()=>checkpointHandoff(item.id);list.append(button);}}
async function checkpointHandoff(id){try{const result=await api('/api/handoff?checkpoint='+encodeURIComponent(id));$('#handoff-text').value=result.text;$('#handoff-dialog').showModal();}catch(e){toast(e.message);}}
$('#project-handoff-open').onclick=()=>openProjectHandoff().catch(e=>toast(e.message));
$('#checkpoint-create').onclick=async()=>{const button=$('#checkpoint-create');button.disabled=true;try{
 await ensureSaved();await load(true);const title=$('#checkpoint-title').value.trim()||'项目阶段交接';
 if(!checkpointRequest||checkpointRequest.title!==title)checkpointRequest={requestId:crypto.randomUUID(),title,expectedRevision:state.revision};
 const result=await api('/api/checkpoints',checkpointRequest);checkpointRequest=null;await renderCheckpoints();await checkpointHandoff(result.id);
 }catch(e){if(e.status>=400&&e.status<500)checkpointRequest=null;toast(e.message);}finally{button.disabled=false;}};
async function openVersion(a){await ensureSaved();await load(true);const prior=state.versionChoices.find(v=>v.assetId===a.id);versionEdit={assetId:a.id,expectedRevision:state.revision};$('#version-title').textContent=a.title;$('#version-disposition').value=prior?.disposition||'candidate';$('#version-reason').value=prior?.reason||'';$('#version-dialog').showModal();}
$('#version-form').onsubmit=async event=>{event.preventDefault();const button=$('#version-save');button.disabled=true;try{await api('/api/versions',{...versionEdit,disposition:$('#version-disposition').value,reason:$('#version-reason').value});$('#version-dialog').close();await load(true);}catch(e){toast(e.message);}finally{button.disabled=false;}};
async function bootstrapProjects(){
 if(!routedProject&&conversationId){bindingState=await api('/api/binding?conversation='+encodeURIComponent(conversationId));routedProject=bindingState.projectId;if(routedProject)history.replaceState(null,'',projectUrl(routedProject));}
 if(!routedProject){$('#project-name').textContent='空白画布';$('#save-status').textContent='尚未创建项目';$('#binding-status').textContent='新对话从空白开始 · 需要接续时选择已有项目';document.title='空白画布 · SW Canvas';
  for(const id of ['project-open','show-tasks','note-open','import-open','binding-copy','project-handoff-open'])$('#'+id).disabled=true;
  if(new URLSearchParams(location.search).get('projects')==='1')openProjects();return;}
 await load(true);await refreshBinding();
 document.body.classList.remove('canvas-empty');
 if(new URLSearchParams(location.search).get('projects')==='1')openProjects();
}
const canvasReady=bootstrapProjects().catch(e=>{$('#save-status').textContent='连接失败';toast(e.message);});
setInterval(()=>{if(!document.hidden&&routedProject){load().catch(()=>$('#save-status').textContent='服务离线');refreshBinding().catch(()=>{});}},3000);
