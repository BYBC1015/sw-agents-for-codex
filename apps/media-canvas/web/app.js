'use strict';
const $=s=>document.querySelector(s), $$=s=>Array.from(document.querySelectorAll(s));
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
const svgEl=(tag,attrs)=>{const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));return n;};
const statuses={queued:'待 Codex 读取',running:'Codex 处理中',review:'待你确认',done:'已确认',failed:'执行失败',cancelled:'已取消'};
let state=null,selected=new Set(),camera={x:35,y:45,zoom:1},linking=false,linkFrom=null,gesture=null,suppressClick=false;
let draftPatch={},saveTimer,saveChain=Promise.resolve(),pendingWrites=0,unsaved=false,libraryLimit=40,renderPending=false;
let activeAsset=null,activeFrame=0,activeRect=null,annotationStart=null,compareAssets=[],toastTimer,frameTimer;
let frameToken=0,frameReady=false,compareToken=0;
let routedProject=new URLSearchParams(location.search).get('project'),conversationId=new URLSearchParams(location.search).get('conversation'),projectBusy=0;
let loadToken=0,composerKey=null,pendingSubmission=null,submitting=false,projectEditRevision=null;
const board=$('#board'),world=$('#node-world');
const asset=id=>state.assets.find(a=>a.id===id), task=id=>state.tasks.find(t=>t.id===id);
const media=(a,kind)=>'/media/'+a.id+'/'+kind+'?project='+encodeURIComponent(routedProject);
const chosenAssets=()=>state.nodes.filter(n=>selected.has(n.id)&&n.kind==='asset').map(n=>asset(n.assetId));
const chosenInputs=()=>state.nodes.filter(n=>selected.has(n.id)&&['asset','note'].includes(n.kind)).map(n=>n.id);
const note=id=>state.notes.find(n=>n.id===id);
function toast(message){clearTimeout(toastTimer);$('#toast').textContent=message;$('#toast').hidden=false;toastTimer=setTimeout(()=>$('#toast').hidden=true,5000);}
async function api(path,body){
 const url=new URL(path,location.origin);
 const globalRoute=['/api/health','/api/projects','/api/projects/new','/api/projects/open','/api/binding','/api/bind'].includes(url.pathname);
 if(!globalRoute){if(!routedProject)throw new Error('请先选择项目');if(body===undefined){if(!url.searchParams.has('project'))url.searchParams.set('project',routedProject);}else body={projectId:routedProject,...body};}
 if(body!==undefined)projectBusy++;
 try{const response=await fetch(url,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json','X-Canvas-Client':'web'},body:JSON.stringify(body),keepalive:JSON.stringify(body).length<50000});
 const data=await response.json();if(!response.ok){const error=new Error(data.error||'请求失败');error.status=response.status;throw error;}return data;}finally{if(body!==undefined)projectBusy--;}
}
function saveBoard(patch){
 loadToken++;
 draftPatch={...draftPatch,...patch,positions:{...(draftPatch.positions||{}),...(patch.positions||{})}};
 unsaved=true;$('#save-status').textContent='保存中…';clearTimeout(saveTimer);saveTimer=setTimeout(flushSave,220);
}
function flushSave(){
 clearTimeout(saveTimer);if(!Object.keys(draftPatch).length)return saveChain;
 const patch=draftPatch;draftPatch={};pendingWrites++;
 saveChain=saveChain.then(()=>api('/api/board',patch)).then(()=>{
   pendingWrites--;unsaved=pendingWrites>0||Object.keys(draftPatch).length>0;
   $('#save-status').textContent=unsaved?'保存中…':'已保存到本机';
 }).catch(error=>{pendingWrites--;draftPatch={...patch,...draftPatch,positions:{...(patch.positions||{}),...(draftPatch.positions||{})}};unsaved=true;$('#save-status').textContent='保存失败 · 点击重试';toast(error.message);});
 return saveChain;
}
$('#save-status').addEventListener('click',()=>{if(unsaved)flushSave();});
window.addEventListener('beforeunload',event=>{if(unsaved){event.preventDefault();event.returnValue='';}});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&unsaved)flushSave();});
async function load(force=false){
 if(pendingWrites||unsaved||gesture)return;
 const token=++loadToken;
 const data=await api('/api/state'+(!force&&state?'?revision='+state.revision:''));
 if(data.unchanged||token!==loadToken||pendingWrites||unsaved||gesture)return;
 state=data;selected=new Set(state.selected);camera=state.camera;
 if(!composerKey){composerKey='media-canvas-composer:'+state.projectId;restoreComposer();}
 $('#project-name').textContent=state.name;document.title=state.name+' · 制作画布';
 $('#project-constraints').textContent=state.constraints.join('\n');
 renderLibrary();renderInspector();renderTasks();scheduleRender();
 $('#asset-count').textContent=state.assets.length;$('#task-count').textContent=state.tasks.filter(t=>!['done','cancelled'].includes(t.status)).length;
 $('#save-status').textContent='已保存到本机';
 $('#undo-layout').disabled=!state.layoutUndo;
}
function scheduleRender(){if(renderPending)return;renderPending=true;requestAnimationFrame(()=>{renderPending=false;renderCanvas();});}
function visible(n){const z=camera.zoom,w=board.clientWidth,h=board.clientHeight;return n.x*z+camera.x>-280*z&&n.x*z+camera.x<w+60&&n.y*z+camera.y>-260*z&&n.y*z+camera.y<h+80;}
function nodeTitle(n){if(n.kind==='asset'){const a=asset(n.assetId);return a.title+(a.version?' · V'+a.version:'');}if(n.kind==='note')return note(n.noteId).title;const t=task(n.taskId||n.resultTaskId);return t.ref+' · '+(n.kind==='result'?'Codex 结果':t.intent==='discuss'?'讨论':'执行任务');}
const cardText=value=>{const chars=Array.from(value||'');return chars.length>120?chars.slice(0,120).join('')+'…':value||'';};
function createNode(n){
 const div=el('article','node '+n.kind);div.dataset.id=n.id;div.draggable=false;
 const header=el('button','node-header');header.type='button';header.draggable=false;header.title=nodeTitle(n);header.append(el('span','',nodeTitle(n)));
 if(n.kind==='asset'){
   const a=asset(n.assetId);header.append(el('small','',a.kind==='video'?'视频':'图片'));div.append(header);
   const img=el('img');img.draggable=false;img.src=media(a,'thumb');img.alt=a.title;img.loading='lazy';img.decoding='async';div.append(img);
   const foot=el('div','node-footer');foot.append(el('span','state',a.status),el('span','meta',a.kind==='video'?`${a.width} × ${a.height} · ${a.fps.toFixed(2).replace('.00','')} fps · ${a.duration.toFixed(2)}s`:`${a.width} × ${a.height}`));div.append(foot);
 }else if(n.kind==='note'){
   header.append(el('small','','文字'));div.append(header,el('div','node-body',cardText(note(n.noteId).text)));
 }else{
   const t=task(n.taskId||n.resultTaskId);header.append(el('small','',statuses[t.status]));div.append(header,el('div','node-body',cardText(n.kind==='result'?t.result||'':t.text)));
 }
 div.addEventListener('click',event=>{if(suppressClick){suppressClick=false;return;}if(linking){linkNode(n.id);return;}selectNode(n.id,event.shiftKey);});
 div.addEventListener('dblclick',()=>{if(n.kind==='asset')openPreview(asset(n.assetId));else if(n.kind==='note'){selectNode(n.id);}else{$('#tasks-dialog').showModal();renderTasks();}});
 return div;
}
function renderCanvas(){
 if(!state)return;
 const live=new Set();let count=0;
 for(const n of state.nodes){
   if(!visible(n)&&!(gesture&&gesture.type==='nodes'&&(selected.has(n.id)||gesture.nodeId===n.id)))continue;
   live.add(n.id);count++;let div=world.querySelector('[data-id="'+n.id+'"]');
   if(!div){div=createNode(n);world.append(div);}
   div.style.transform=`translate3d(${n.x*camera.zoom+camera.x}px,${n.y*camera.zoom+camera.y}px,0) scale(${camera.zoom})`;div.classList.toggle('selected',selected.has(n.id));
   div.querySelector('.node-header span').textContent=nodeTitle(n);div.querySelector('.node-header').title=nodeTitle(n);
   div.querySelector('button').setAttribute('aria-pressed',String(selected.has(n.id)));
   if(n.kind==='asset'){const a=asset(n.assetId);div.querySelector('.state').textContent=a.status+(a.disposition?' · '+({candidate:'候选',selected:'已选定',rejected:'未采用',delivered:'已交付'}[a.disposition]):'');}
   else if(n.kind==='note'){div.querySelector('.node-body').textContent=cardText(note(n.noteId).text);}
   else if(n.kind!=='asset'){const t=task(n.taskId||n.resultTaskId);div.querySelector('small').textContent=statuses[t.status];div.querySelector('.node-body').textContent=cardText(n.kind==='result'?t.result||'':t.text);}
 }
 Array.from(world.children).forEach(n=>{if(!live.has(n.dataset.id))n.remove();});
 const group=$('#edge-group');group.replaceChildren();group.setAttribute('transform',`translate(${camera.x} ${camera.y}) scale(${camera.zoom})`);
 for(const edge of state.edges){
   if(!live.has(edge.source)&&!live.has(edge.target))continue;
   const a=state.nodes.find(n=>n.id===edge.source),b=state.nodes.find(n=>n.id===edge.target);if(!a||!b)continue;
   const vertical=Math.abs(a.x-b.x)<200;
   let sx=a.x+250,sy=a.y+CanvasGeometry.height(a)/2,tx=b.x,ty=b.y+CanvasGeometry.height(b)/2,d;
   if(vertical){const down=b.y>a.y;sx=a.x+125;sy=a.y+(down?CanvasGeometry.height(a):0);tx=b.x+125;ty=b.y+(down?0:CanvasGeometry.height(b));const mid=(sy+ty)/2;d=`M ${sx} ${sy} C ${sx} ${mid} ${tx} ${mid} ${tx} ${ty}`;}
   else{const mid=(sx+tx)/2;d=`M ${sx} ${sy} C ${mid} ${sy} ${mid} ${ty} ${tx} ${ty}`;}
   group.append(svgEl('path',{d}));const label=svgEl('text',{x:(sx+tx)/2+(vertical?8:0),y:(sy+ty)/2-9,'text-anchor':vertical?'start':'middle'});label.textContent=edge.label;group.append(label);
 }
 $('#zoom-label').textContent=Math.round(camera.zoom*100)+'%';$('#visible-count').textContent=`当前渲染 ${count} / ${state.nodes.length} 个节点`;
 $('#selection-label').textContent=selected.size?`已选 ${selected.size} 个节点`:'镜头与版本关系';
}
function selectNode(id,toggle=false){
 if(toggle){if(selected.has(id))selected.delete(id);else selected.add(id);}else selected=new Set([id]);
 state.selected=Array.from(selected);saveBoard({selected:state.selected});renderInspector();scheduleRender();
}
function centerNode(id){const n=state.nodes.find(n=>n.id===id);if(!n)return;camera.x=board.clientWidth/2-(n.x+125)*camera.zoom;camera.y=board.clientHeight/2-(n.y+115)*camera.zoom;selectNode(id);saveBoard({camera:{...camera}});}
function fitView(){
 if(!state?.nodes.length)return;
 const xs=state.nodes.map(n=>n.x),ys=state.nodes.map(n=>n.y),minX=Math.min(...xs),minY=Math.min(...ys),w=Math.max(...xs)+250-minX,h=Math.max(...state.nodes.map(n=>n.y+CanvasGeometry.height(n)))-minY;
 camera.zoom=Math.max(.25,Math.min(1,(board.clientWidth-55)/w,(board.clientHeight-65)/h));camera.x=(board.clientWidth-w*camera.zoom)/2-minX*camera.zoom;camera.y=(board.clientHeight-h*camera.zoom)/2-minY*camera.zoom;
 saveBoard({camera:{...camera}});scheduleRender();
}
function zoomAt(factor,x=board.clientWidth/2,y=board.clientHeight/2){const z=Math.max(.25,Math.min(2,camera.zoom*factor));camera.x=x-(x-camera.x)*z/camera.zoom;camera.y=y-(y-camera.y)*z/camera.zoom;camera.zoom=z;scheduleRender();saveBoard({camera:{...camera}});}
board.addEventListener('wheel',event=>{if(!state)return;event.preventDefault();const r=board.getBoundingClientRect();zoomAt(Math.exp(-event.deltaY*.0013),event.clientX-r.left,event.clientY-r.top);},{passive:false});
$('#zoom-in').onclick=()=>zoomAt(1.2);$('#zoom-out').onclick=()=>zoomAt(1/1.2);$('#fit-view').onclick=fitView;
async function applyLayout(action){
 const button=action==='undo'?$('#undo-layout'):$('#arrange-view');button.disabled=true;
 try{await ensureSaved();await load(true);await api('/api/layout',{action,expectedRevision:state.revision});await load(true);fitView();toast(action==='undo'?'已撤销排布':'已按参考 → 任务 → 产出 → 结果说明排布');}
 catch(e){toast(e.message);}finally{$('#arrange-view').disabled=false;$('#undo-layout').disabled=!state?.layoutUndo;}
}
$('#arrange-view').onclick=()=>applyLayout('arrange');$('#undo-layout').onclick=()=>applyLayout('undo');
board.addEventListener('dragstart',event=>event.preventDefault());
board.addEventListener('pointerdown',event=>{
 if(!state||linking||gesture||event.button!==0)return;
 const node=event.target.closest('.node'),header=event.target.closest('.node-header');if(node&&!header)return;
 const rect=board.getBoundingClientRect();const x=event.clientX-rect.left,y=event.clientY-rect.top;
 event.preventDefault();window.getSelection()?.removeAllRanges();loadToken++;
 gesture={pointerId:event.pointerId,x,y,lastX:x,lastY:y,moved:false,type:node?'nodes':event.shiftKey?'marquee':'pan',nodeId:node?.dataset.id,baseCamera:{...camera},positions:null,baseSelected:new Set(selected)};
 gesture.capture=node||board;gesture.capture.setPointerCapture(event.pointerId);
});
board.addEventListener('pointermove',event=>{
 if(!gesture||event.pointerId!==gesture.pointerId)return;event.preventDefault();const rect=board.getBoundingClientRect(),x=event.clientX-rect.left,y=event.clientY-rect.top,dx=x-gesture.x,dy=y-gesture.y;
 if(Math.abs(dx)+Math.abs(dy)>4)gesture.moved=true;if(!gesture.moved)return;
 if(gesture.type==='nodes'){
   if(!gesture.positions){if(!selected.has(gesture.nodeId)){selected=new Set([gesture.nodeId]);renderInspector();}gesture.positions=Object.fromEntries(state.nodes.filter(n=>selected.has(n.id)).map(n=>[n.id,{x:n.x,y:n.y}]));}
   state.nodes.forEach(n=>{const p=gesture.positions[n.id];if(p){n.x=p.x+dx/camera.zoom;n.y=p.y+dy/camera.zoom;}});
 }else if(gesture.type==='pan'){camera.x=gesture.baseCamera.x+dx;camera.y=gesture.baseCamera.y+dy;}
 else{const box=$('#marquee');box.hidden=false;Object.assign(box.style,{left:Math.min(x,gesture.x)+'px',top:Math.min(y,gesture.y)+'px',width:Math.abs(dx)+'px',height:Math.abs(dy)+'px'});}
 gesture.lastX=x;gesture.lastY=y;scheduleRender();
});
function endGesture(event){
 if(!gesture||event&&event.pointerId!==gesture.pointerId)return;const g=gesture;gesture=null;$('#marquee').hidden=true;
 if(g.capture.hasPointerCapture(g.pointerId))g.capture.releasePointerCapture(g.pointerId);
 if(event&&event.type!=='pointerup'){
  if(g.positions)for(const n of state.nodes){if(g.positions[n.id])Object.assign(n,g.positions[n.id]);}
  camera=g.baseCamera;selected=g.baseSelected;scheduleRender();renderInspector();return;
 }
 if(g.moved){suppressClick=true;setTimeout(()=>suppressClick=false,100);
   if(g.type==='nodes'){CanvasGeometry.settle(state.nodes,selected);const positions=Object.fromEntries(state.nodes.filter(n=>selected.has(n.id)).map(n=>[n.id,{x:n.x,y:n.y}]));saveBoard({positions,selected:Array.from(selected)});}
   else if(g.type==='pan')saveBoard({camera:{...camera}});
   else{const l=(Math.min(g.x,g.lastX)-camera.x)/camera.zoom,t=(Math.min(g.y,g.lastY)-camera.y)/camera.zoom,r=(Math.max(g.x,g.lastX)-camera.x)/camera.zoom,b=(Math.max(g.y,g.lastY)-camera.y)/camera.zoom;state.nodes.forEach(n=>{if(n.x+250>l&&n.x<r&&n.y+CanvasGeometry.height(n)>t&&n.y<b)selected.add(n.id);});saveBoard({selected:Array.from(selected)});renderInspector();}
   scheduleRender();
 }else if(g.type==='pan'){selected.clear();saveBoard({selected:[]});renderInspector();scheduleRender();}
}
board.addEventListener('pointerup',endGesture);board.addEventListener('pointercancel',endGesture);board.addEventListener('lostpointercapture',endGesture);
new ResizeObserver(scheduleRender).observe(board);
function setLinking(value){linking=value;linkFrom=null;$('#link-mode').setAttribute('aria-pressed',String(value));$('#canvas-mode').hidden=!value;$('#canvas-mode').textContent='依次点击两个节点建立参考关系';board.classList.toggle('is-linking',value);}
$('#link-mode').onclick=()=>setLinking(!linking);
async function linkNode(id){if(!linkFrom){linkFrom=id;$('#canvas-mode').textContent='起点已选，点击另一个节点';return;}if(linkFrom===id){toast('请选择另一个节点');return;}const edge={source:linkFrom,target:id};setLinking(false);try{await flushSave();await api('/api/board',{edge});await load(true);}catch(e){toast(e.message);}}
function renderLibrary(){
 const list=$('#library-list');list.replaceChildren();const query=$('#asset-search').value.trim().toLowerCase();const assets=state.assets.filter(a=>(a.title+' '+a.fileName).toLowerCase().includes(query));
 assets.slice(0,libraryLimit).forEach(a=>{const button=el('button','library-item');const img=el('img');img.src=media(a,'thumb');img.alt='';img.loading='lazy';const info=el('span');info.append(el('strong','',a.title),el('small','',a.group));button.append(img,info);button.onclick=()=>centerNode(state.nodes.find(n=>n.assetId===a.id).id);list.append(button);});
 $('#library-more').hidden=assets.length<=libraryLimit;
}
$('#asset-search').oninput=()=>{libraryLimit=40;renderLibrary();};$('#library-more').onclick=()=>{libraryLimit+=40;renderLibrary();};
function renderInspector(){
 const box=$('#inspector-content');box.replaceChildren();const nodes=state.nodes.filter(n=>selected.has(n.id));const assets=chosenAssets();$('#submit-task').disabled=$('#discuss-task').disabled=submitting||!chosenInputs().length;$('#compare-open').disabled=assets.length!==2;
 if(!nodes.length){box.append(el('div','empty','选择一个素材查看详情。Shift 点选可同时选择多个版本。'));return;}
 if(nodes.length>1){box.append(el('h3','',`${nodes.length} 个节点已选中`));nodes.forEach(n=>box.append(el('p','metadata',nodeTitle(n))));return;}
 const n=nodes[0];
 if(n.kind==='asset'){
   const a=asset(n.assetId);box.append(el('h3','',a.title),el('span','status-chip',a.status));const img=el('img','poster');img.src=media(a,'thumb');img.alt=a.title;box.append(img);
   box.append(el('div','metadata',a.kind==='video'?`${a.width} × ${a.height} / ${a.fps} fps / ${a.frames} 帧`:`${a.width} × ${a.height}`));
   const preview=el('button','full','预览与圈注');preview.onclick=()=>openPreview(a);box.append(preview);const version=el('button','full','标记版本取舍');version.onclick=()=>openVersion(a).catch(e=>toast(e.message));box.append(version);
   const details=el('details');details.append(el('summary','','原始文件位置'),el('p','',a.path));box.append(details);
   const notes=state.annotations.filter(v=>v.assetId===a.id);if(notes.length)box.append(el('div','section-heading',`标注 · ${notes.length}`));
   notes.slice(-8).forEach(note=>{const div=el('div','note');div.append(el('small','',`F${note.frame}${note.rect?' · 有区域标记':''}`),el('span','',note.text));box.append(div);});
 }else if(n.kind==='note'){const item=note(n.noteId);box.append(el('h3','',item.title),el('p','result-text',item.text));}
 else{const t=task(n.taskId||n.resultTaskId);box.append(el('h3','',nodeTitle(n)),el('span','status-chip',statuses[t.status]),el('p','result-text',n.kind==='result'?t.result||'':t.text));const b=el('button','full','查看任务详情');b.onclick=()=>{renderTasks();$('#tasks-dialog').showModal();};box.append(b);}
}
async function ensureSaved(){await flushSave();if(unsaved)throw new Error('布局尚未保存，请先点击保存状态重试。');}
async function submitTask(intent){
 if(submitting||!chosenInputs().length)return;
 if(pendingSubmission){toast('上次提交尚未确认，请先点击「重试上次提交」。');return;}
 const text=$('#task-text').value.trim()||(intent==='discuss'?'请讨论所选内容，不执行制作任务。':'');
 const nodeIds=chosenInputs(),frameRange=$('#task-frames').value;
 if(!text){toast('请填写修改要求');$('#task-text').focus();return;}
 try{
   await ensureSaved();
   pendingSubmission={projectId:state.projectId,requestId:crypto.randomUUID(),nodeIds,text,frameRange,intent};
   if(!saveComposer())throw new Error('浏览器无法保存提交编号，请保留要求文字并检查存储权限。');
   await sendSubmission();
 }catch(e){toast(e.message);}
}
async function sendSubmission(){
 if(submitting||!pendingSubmission)return;
 if(!saveComposer()){toast('无法保存提交编号，请检查浏览器存储权限。');return;}
 submitting=true;renderInspector();$('#retry-task').disabled=true;
 const body=structuredClone(pendingSubmission);
 try{
   const created=await api('/api/tasks',body);pendingSubmission=null;
   if($('#task-text').value.trim()===body.text||!$('#task-text').value.trim()){$('#task-text').value='';$('#task-frames').value='';}
   saveComposer();await load(true);await showHandoff(created.ref);
 }catch(e){if(e.status>=400&&e.status<500&&![408,429].includes(e.status)){pendingSubmission=null;saveComposer();}toast(e.message);}
 finally{submitting=false;$('#retry-task').disabled=false;renderInspector();}
}
$('#submit-task').onclick=()=>submitTask('execute');$('#discuss-task').onclick=()=>submitTask('discuss');
$('#retry-task').onclick=()=>sendSubmission();
function saveComposer(){
 $('#retry-task').hidden=!pendingSubmission;
 if(!composerKey)return false;
 try{localStorage.setItem(composerKey,JSON.stringify({text:$('#task-text').value,frames:$('#task-frames').value,pending:pendingSubmission}));return true;}catch{return false;}
}
function restoreComposer(){
 try{const compose=JSON.parse(localStorage.getItem(composerKey)||(location.port==='8961'?localStorage.getItem('media-canvas-composer'):null)||'{}');$('#task-text').value=compose.text||'';$('#task-frames').value=compose.frames||'';pendingSubmission=compose.pending||null;$('#retry-task').hidden=!pendingSubmission;}catch{}
}
$('#task-text').addEventListener('input',saveComposer);$('#task-frames').addEventListener('input',saveComposer);
async function showHandoff(id){
 const query=new URLSearchParams({project:state.projectId});if(id)query.set('task',id);
 const result=await api('/api/handoff?'+query);$('#handoff-text').value=result.text;
 if(!$('#handoff-dialog').open)$('#handoff-dialog').showModal();
}
async function copyText(text){try{await navigator.clipboard.writeText(text);toast('指令已复制，可以粘贴到 Codex。');}catch{toast('剪贴板不可用，请选中上方指令手动复制。');}}
$('#handoff-copy').onclick=()=>copyText($('#handoff-text').value);
$('#copy-context').onclick=()=>showHandoff().catch(e=>toast(e.message));
let noteRequest=null;
$('#note-open').onclick=()=>$('#note-dialog').showModal();
$('#note-form').onsubmit=async event=>{
 event.preventDefault();const button=$('#note-submit');button.disabled=true;
 const body={title:$('#note-title').value.trim(),text:$('#note-text').value.trim(),nodeIds:Array.from(selected)};
 const signature=JSON.stringify(body);
 if(!noteRequest||noteRequest.signature!==signature)noteRequest={signature,id:crypto.randomUUID()};
 try{await ensureSaved();const result=await api('/api/notes',{...body,requestId:noteRequest.id});noteRequest=null;$('#note-title').value='';$('#note-text').value='';$('#note-dialog').close();await load(true);centerNode(result.nodeId);toast('文字已加入画布。');}catch(e){toast(e.message);}finally{button.disabled=false;}
};
$('#project-open').onclick=async()=>{
 try{await ensureSaved();await load(true);projectEditRevision=state.revision;
 $('#project-id').textContent=state.projectId+' · 独立项目数据';
 for(const [field,key] of [['title','name'],['goal','goal'],['decisions','decisions'],['next','nextStep']])$('#project-'+field).value=state[key]||'';
 $('#project-rules').value=state.constraints.join('\n');for(const key of ['stage','blockers','openQuestions','deliveryNotes'])$('#progress-'+key).value=state.progress[key]||'';$('#project-dialog').showModal();
 }catch(e){toast(e.message);}
};
$('#project-form').onsubmit=async event=>{
 event.preventDefault();const button=$('#project-submit');button.disabled=true;
 try{await api('/api/project',{expectedRevision:projectEditRevision,name:$('#project-title').value,goal:$('#project-goal').value,decisions:$('#project-decisions').value,nextStep:$('#project-next').value,constraints:$('#project-rules').value.split(/\r?\n/).map(s=>s.trim()).filter(Boolean),progress:Object.fromEntries(['stage','blockers','openQuestions','deliveryNotes'].map(k=>[k,$('#progress-'+k).value]))});$('#project-dialog').close();await load(true);toast('项目摘要已保存，新对话可以读取。');}catch(e){toast(e.message);}finally{button.disabled=false;}
};
function renderTasks(){
 const list=$('#tasks-list');list.replaceChildren();if(!state.tasks.length){list.append(el('p','empty','尚无任务。选择素材并填写修改要求即可创建。'));return;}
 [...state.tasks].reverse().forEach(t=>{
   const row=el('section','task-row'),head=el('div','task-row-header');head.append(el('strong','',t.ref+' · '+(t.intent==='discuss'?'讨论':'执行')),el('span','status-chip',statuses[t.status]),el('small','',new Date(t.createdAt).toLocaleString('zh-CN')));row.append(head,el('h3','',t.text),el('small','',t.input.assets.map(a=>a.title).concat((t.input.notes||[]).map(n=>n.title)).join('、')+(t.frameRange?' / '+t.frameRange:'')));
   if(t.result)row.append(el('p','task-result',t.result));const actions=el('div','actions');const copy=el('button','','接续此任务');copy.onclick=()=>showHandoff(t.ref).catch(e=>toast(e.message));actions.append(copy);
   for(const aid of t.outputAssetIds||[]){const a=asset(aid);if(!a)continue;const b=el('button','','定位输出：'+a.title);b.onclick=()=>{$('#tasks-dialog').close();centerNode(state.nodes.find(n=>n.assetId===aid).id);};actions.append(b);}
   const details=el('details');details.append(el('summary','small muted','查看提交时的素材与标注快照'),el('pre','result-text',JSON.stringify({assets:t.input.assets.map(a=>({title:a.title,path:a.path,id:a.id})),notes:t.input.notes||[],annotations:t.input.annotations},null,2)));row.append(details);
   const action=t.status==='queued'?['取消任务','cancelled']:t.status==='review'?['确认结果','done']:t.status==='failed'?['重新排队','queued']:null;
   if(action){const b=el('button','',action[0]);b.onclick=async()=>{b.disabled=true;try{await api('/api/task-action',{id:t.id,status:action[1]});await load(true);}catch(e){toast(e.message);b.disabled=false;}};actions.append(b);}
   row.append(actions);list.append(row);
 });
}
$('#show-tasks').onclick=()=>{renderTasks();$('#tasks-dialog').showModal();};
$$('[data-close]').forEach(b=>b.onclick=()=>document.getElementById(b.dataset.close).close());
$('#import-open').onclick=()=>$('#import-dialog').showModal();
$('#import-form').onsubmit=async event=>{
 event.preventDefault();const paths=$('#import-paths').value.split(/\r?\n/).map(s=>s.trim().replace(/^"|"$/g,'')).filter(Boolean);if(!paths.length)return;
 const b=$('#import-submit');b.disabled=true;$('#import-status').textContent='正在登记素材，视频预览可能需要一些时间…';
 try{const files=paths.map(path=>({path,mode:$('#import-mode').value})),key='sw-canvas-import:'+state.projectId,signature=JSON.stringify(files);let pending=JSON.parse(localStorage.getItem(key)||'null');
 if(!pending||pending.signature!==signature){pending={signature,requestId:crypto.randomUUID()};localStorage.setItem(key,JSON.stringify(pending));}
 await api('/api/ingest',{requestId:pending.requestId,files});localStorage.removeItem(key);await load(true);$('#import-paths').value='';$('#import-status').textContent='';$('#import-dialog').close();fitView();toast(`已导入 ${paths.length} 项素材`);
 }catch(e){$('#import-status').textContent=e.message;}finally{b.disabled=false;}
};
function openPreview(a){
 activeAsset=a;activeFrame=0;activeRect=null;$('#preview-title').textContent=a.title;$('#original-link').href=media(a,'original');$('#annotation-text').value='';
 const video=$('#preview-video');video.pause();video.removeAttribute('src');video.poster=media(a,'thumb');
 if(a.kind==='video')video.src=media(a,'preview');
 $('#play-mode').hidden=a.kind!=='video';$('#frame-number').max=$('#frame-slider').max=Math.max(0,a.frames-1);$('#frame-number').value=$('#frame-slider').value='0';
 setPreviewMode(a.kind==='video'?'play':'frame');$('#preview-dialog').showModal();
}
function setPreviewMode(mode){
 const frame=mode==='frame';$('#preview-video').hidden=frame;$('#frame-panel').hidden=!frame;$('#play-mode').setAttribute('aria-pressed',String(!frame));$('#frame-mode').setAttribute('aria-pressed',String(frame));
 if(frame){$('#preview-video').pause();updateFrame();}
}
$('#play-mode').onclick=()=>setPreviewMode('play');$('#frame-mode').onclick=()=>setPreviewMode('frame');
$('#preview-dialog').addEventListener('close',()=>{frameToken++;frameReady=false;clearTimeout(frameTimer);const v=$('#preview-video');v.pause();v.removeAttribute('src');v.load();$('#frame-image').removeAttribute('src');activeAsset=null;});
function loadImage(url){return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>resolve(url);img.onerror=()=>reject(new Error('无法读取目标帧，请检查原文件是否仍在原位。'));img.src=url;});}
function blockFrame(){frameReady=false;$('#save-annotation').disabled=true;$('#frame-image').hidden=true;$('#annotation-overlay').toggleAttribute('hidden',true);$('#frame-loading').hidden=false;$('#frame-loading').textContent='正在从原片读取 F'+activeFrame+'…';}
function updateFrame(){
 if(!activeAsset)return;const token=++frameToken;activeRect=null;annotationStart=null;blockFrame();$('#frame-number').value=$('#frame-slider').value=activeFrame;
 loadImage(media(activeAsset,'frame')+'&n='+activeFrame).then(url=>{if(token!==frameToken||!activeAsset)return;$('#frame-image').src=url;$('#frame-image').alt='原片第 '+activeFrame+' 帧';$('#frame-image').hidden=false;$('#annotation-overlay').toggleAttribute('hidden',false);$('#frame-loading').hidden=true;frameReady=true;$('#save-annotation').disabled=false;drawAnnotations();}).catch(e=>{if(token===frameToken)$('#frame-loading').textContent=e.message;});
 const notes=$('#frame-notes');notes.replaceChildren();state.annotations.filter(n=>n.assetId===activeAsset.id&&n.frame===activeFrame).forEach(n=>notes.append(el('p','',n.text)));
}
$('#frame-image').onerror=()=>toast('此帧暂时无法读取，请检查原文件是否仍在原位。');
function setFrame(value){if(!activeAsset)return;const n=Number(value);if(!Number.isFinite(n))return;activeFrame=Math.max(0,Math.min(activeAsset.frames-1,Math.round(n)));frameToken++;blockFrame();clearTimeout(frameTimer);frameTimer=setTimeout(updateFrame,100);}
$('#frame-number').onchange=e=>setFrame(e.target.value);$('#frame-slider').oninput=e=>setFrame(e.target.value);
function drawAnnotations(){
 const overlay=$('#annotation-overlay');overlay.replaceChildren();if(!activeAsset)return;
 const rects=state.annotations.filter(n=>n.assetId===activeAsset.id&&n.frame===activeFrame&&n.rect).map(n=>n.rect);if(activeRect)rects.push(activeRect);
 rects.forEach(r=>overlay.append(svgEl('rect',{x:r[0],y:r[1],width:r[2],height:r[3]})));
}
const overlay=$('#annotation-overlay');
function normalPoint(e){const r=overlay.getBoundingClientRect();return [Math.max(0,Math.min(1,(e.clientX-r.left)/r.width)),Math.max(0,Math.min(1,(e.clientY-r.top)/r.height))];}
overlay.onpointerdown=e=>{if(!frameReady)return;annotationStart=normalPoint(e);activeRect=null;overlay.setPointerCapture(e.pointerId);};
overlay.onpointermove=e=>{if(!annotationStart)return;const p=normalPoint(e);activeRect=[Math.min(p[0],annotationStart[0]),Math.min(p[1],annotationStart[1]),Math.abs(p[0]-annotationStart[0]),Math.abs(p[1]-annotationStart[1])];drawAnnotations();};
overlay.onpointerup=overlay.onpointercancel=()=>{annotationStart=null;if(activeRect&&(activeRect[2]<.002||activeRect[3]<.002)){activeRect=null;drawAnnotations();}};
$('#clear-rect').onclick=()=>{activeRect=null;drawAnnotations();};
$('#save-annotation').onclick=async()=>{
 if(!frameReady)return;const text=$('#annotation-text').value.trim();if(!text){toast('请填写标注意见');return;}const b=$('#save-annotation');b.disabled=true;
 try{await api('/api/annotations',{assetId:activeAsset.id,frame:activeFrame,rect:activeRect,text});$('#annotation-text').value='';await load(true);updateFrame();toast('标注已保存，下次提交此素材时会一起交给 Codex。');}catch(e){toast(e.message);}finally{b.disabled=!frameReady;}
};
$('#compare-open').onclick=()=>{
 compareAssets=chosenAssets();if(compareAssets.length!==2){toast('请按 Shift 选择两个素材节点');return;}
 const max=Math.max(0,Math.min(...compareAssets.filter(a=>a.kind==='video').map(a=>a.frames-1),10000000));
 $('#compare-frame').max=$('#compare-slider').max=max===10000000?0:max;$('#compare-frame').value=$('#compare-slider').value=0;
 const panes=$('#compare-panes');panes.replaceChildren();compareAssets.forEach(a=>{const pane=el('section');const img=el('img');img.alt=a.title;img.dataset.asset=a.id;pane.append(el('h3','',a.title),img);panes.append(pane);});updateCompare(0);$('#compare-dialog').showModal();
};
function updateCompare(value){
 const n=Math.max(0,Math.min(Number($('#compare-frame').max),Math.round(Number(value)||0))),token=++compareToken;
 $('#compare-frame').value=$('#compare-slider').value=n;$('#compare-loading').textContent='正在读取 F'+n+' 的两个素材…';$$('#compare-panes img').forEach(img=>img.hidden=true);
 Promise.all(compareAssets.map(a=>loadImage(media(a,'frame')+'&n='+(a.kind==='image'?0:n)))).then(urls=>{
   if(token!==compareToken)return;compareAssets.forEach((a,i)=>{const img=$('#compare-panes img[data-asset="'+a.id+'"]');img.src=urls[i];img.alt=a.title+' / F'+(a.kind==='image'?0:n);img.hidden=false;});$('#compare-loading').textContent='F'+n+' · 两个素材均已就绪';
 }).catch(e=>{if(token===compareToken)$('#compare-loading').textContent=e.message;});
}
$('#compare-dialog').addEventListener('close',()=>{compareToken++;clearTimeout(compareTimer);});
$('#compare-frame').onchange=e=>updateCompare(e.target.value);let compareTimer;$('#compare-slider').oninput=e=>{clearTimeout(compareTimer);compareTimer=setTimeout(()=>updateCompare(e.target.value),120);};
document.addEventListener('keydown',e=>{if(e.key==='Escape')setLinking(false);});
// Project bootstrap and polling are installed by projects.js.
