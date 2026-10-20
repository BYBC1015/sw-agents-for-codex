'use strict';
// All text is inserted with textContent. Mutations use the revision captured by the editor.
const storyButton=el('button','','分镜与连续性');
$('.topbar').insertBefore(storyButton,$('#note-open'));
const storyDialog=el('dialog','wide-dialog');
storyDialog.setAttribute('aria-label','分镜与连续性');
document.body.append(storyDialog);
let storyProject=null,storyData=null,storyRevision=null;
const issueText=i=>i.type==='dependency'?`${i.entityId}：使用 v${i.usedVersion}，当前 v${i.currentVersion}`:i.type==='missing-output'?'缺少本镜头版本的输出图':'视觉验收：'+({unchecked:'未检查',fail:'未通过'}[i.status]||i.status);
function storyControl(parent,label,value='',type='text'){
 const wrap=el('label','',label),input=el(type==='textarea'?'textarea':'input');
 if(type!=='textarea')input.type=type;else input.rows=3;
 input.value=value??'';wrap.append(input);parent.append(wrap);return input;
}
function storySelect(parent,label,options,value){
 const wrap=el('label','',label),input=el('select');
 for(const [key,title] of options){const option=el('option','',title);option.value=key;input.append(option);}
 input.value=value??'';wrap.append(input);parent.append(wrap);return input;
}
function storyAction(parent,label,fn,primary=false){
 const button=el('button',primary?'primary':'',label);button.type='button';
 button.onclick=async()=>{button.disabled=true;try{await fn();}catch(e){toast(e.message);}finally{button.disabled=false;}};
 parent.append(button);return button;
}
async function storyWrite(body,expectedRevision=storyRevision){
 if(routedProject!==storyProject)throw new Error('项目已切换，请重新打开分镜');
 await ensureSaved();
 await api('/api/storyboard',{...body,projectId:storyProject,expectedRevision,requestId:crypto.randomUUID()});
 await load(true);await openStory();
}
function storyCurrent(item){return item.versions.find(v=>v.version===item.currentVersion);}
async function openStory(){
 await ensureSaved();const pid=routedProject;if(!pid)throw new Error('请先打开项目');
 const snapshot=await api('/api/state?project='+encodeURIComponent(pid));
 const exported=await api('/api/storyboard-export?project='+encodeURIComponent(pid));
 if(pid!==routedProject)throw new Error('项目已切换');
 if(snapshot.revision!==exported.revision)throw new Error('项目刚刚发生变化，请重新打开分镜');
 storyProject=pid;storyData=snapshot;storyRevision=snapshot.revision;
 storyDialog.replaceChildren();
 const heading=el('div','dialog-heading');heading.append(el('h2','','分镜与连续性'));
 storyAction(heading,'关闭',()=>storyDialog.close());storyDialog.append(heading);
 storyDialog.append(el('p','muted small','逐镜保存版本。公共资产变化只提示待复核，不自动生成。'));
 const toolbar=el('div','story-actions');storyDialog.append(toolbar);
 storyAction(toolbar,'＋ 镜头',()=>editShot());storyAction(toolbar,'＋ 角色 / 场景 / 道具',()=>editEntity());
 storyAction(toolbar,'导出草稿清单',()=>downloadStory(false));storyAction(toolbar,'导出验收清单',()=>downloadStory(true));
 const editor=el('section','story-editor');editor.id='story-editor';storyDialog.append(editor);
 storyDialog.append(el('h3','','公共资产'));
 for(const entity of snapshot.storyboard.entities){
  const row=el('section','story-row'),v=storyCurrent(entity);row.append(el('strong','',`${entity.id} · v${v.version}`),el('p','',v.description));
  storyAction(row,'编辑 / 查看影响',()=>editEntity(entity));storyVersion(row,entity,'entity');storyDialog.append(row);
 }
 storyDialog.append(el('h3','',`${exported.shots.length} 个镜头 · ${exported.totalDuration} 秒`));
 if(!exported.shots.length)storyDialog.append(el('p','muted','添加第一个镜头，或让对话将已确认分镜写入此项目。'));
 for(const shot of exported.shots){
  const row=el('section','story-row');row.append(el('strong','',`${shot.id} · ${shot.title} · v${shot.version}`));
  if(shot.outputAssetId){const output=snapshot.assets.find(a=>a.id===shot.outputAssetId);if(output){const img=el('img','story-thumb');img.src='/media/'+output.id+'/thumb?project='+encodeURIComponent(pid);img.alt=shot.title;row.append(img);}}
  row.append(el('p','',shot.script),el('p','muted small',`${shot.duration} 秒 · ${shot.camera}`));
  row.append(el('p',shot.issues.length?'story-warning':'story-ready',shot.issues.length?shot.issues.map(issueText).join('；'):'已通过视觉验收'));
  storyAction(row,'编辑镜头',()=>editShot(snapshot.storyboard.shots.find(s=>s.id===shot.id)));
  storyAction(row,'记录验收',()=>reviewShot(shot));
  storyVersion(row,snapshot.storyboard.shots.find(s=>s.id===shot.id),'shot');storyDialog.append(row);
 }
 if(!storyDialog.open)storyDialog.showModal();
}
function storyVersion(row,item,kind){
 if(item.versions.length<2)return;
 const select=storySelect(row,'选定版本',item.versions.map(v=>[v.version,'v'+v.version]),item.currentVersion);
 storyAction(row,'切换到此版本',()=>storyWrite({action:'select',id:item.id,kind,version:Number(select.value)}));
}
function storyEditor(title){const form=el('form');form.append(el('h3','',title));const area=$('#story-editor');area.replaceChildren(form);area.scrollIntoView({block:'nearest'});return form;}
function storySave(form,fn){const save=el('button','primary','保存新版本');save.type='submit';form.append(save);form.onsubmit=async e=>{e.preventDefault();save.disabled=true;try{await fn();}catch(error){toast(error.message);}finally{save.disabled=false;}};}
function editEntity(entity){
 const revision=storyRevision,v=entity?storyCurrent(entity):{},form=storyEditor('公共资产与锁定项');
 const id=storyControl(form,'稳定编号',entity?.id||'');id.required=true;id.readOnly=!!entity;
 const kind=storySelect(form,'资产类型',[['character','角色'],['wardrobe','服装'],['scene','场景'],['prop','道具'],['product','产品'],['style','风格']],entity?.kind||'character');kind.disabled=!!entity;
 const description=storyControl(form,'设定说明',v.description||'','textarea');description.required=true;
 const lock=storyControl(form,'必须保留的细节（每行一条）',(v.locks||[]).join('\n'),'textarea');
 const ref=storySelect(form,'参考素材',[['','暂未指定'],...storyData.assets.map(a=>[a.id,a.title])],v.assetId||'');
 if(entity){const affected=storyData.storyboard.shots.filter(s=>Object.hasOwn(storyCurrent(s).entityRefs,entity.id));form.append(el('p','story-warning','修改后需要复核：'+(affected.map(s=>s.id).join('、')||'暂无引用镜头')));}
 storySave(form,()=>storyWrite({action:'entity',id:id.value,kind:kind.value,fields:{description:description.value,locks:lock.value.split('\n').map(x=>x.trim()).filter(Boolean),assetId:ref.value||null}},revision));
}
function editShot(shot){
 const revision=storyRevision,v=shot?storyCurrent(shot):{},form=storyEditor('镜头记录');
 const id=storyControl(form,'镜头编号',shot?.id||'');id.required=true;id.readOnly=!!shot;
 const title=storyControl(form,'标题',v.title||'');title.required=true;
 const script=storyControl(form,'剧本 / 画面',v.script||'','textarea');
 const duration=storyControl(form,'时长（秒）',v.duration||5,'number');duration.min='.01';duration.max='3600';duration.step='.01';
 const camera=storyControl(form,'机位 / 景别 / 运镜',v.camera||'','textarea');
 const lock=storyControl(form,'本镜头锁定项（每行一条）',(v.locks||[]).join('\n'),'textarea');
 const refs=[];
 for(const entity of storyData.storyboard.entities){
  const used=v.entityRefs?.[entity.id];
  const selector=storySelect(form,entity.id,[['','不引用'],...entity.versions.map(r=>[r.version,`v${r.version}${r.version===entity.currentVersion?'（当前）':''} · ${r.description.slice(0,60)}`])],used||'');refs.push([entity.id,selector]);
 }
 const output=storySelect(form,'输出素材',[['','待生成'],...storyData.assets.map(a=>[a.id,a.title])],v.outputAssetId||'');
 form.append(el('p','muted small','改变画面、机位、引用或锁定项时，原输出自动解除关联。请选择真正对应新版本的输出。'));
 storySave(form,()=>{
  const fields={title:title.value,script:script.value,duration:Number(duration.value),camera:camera.value,locks:lock.value.split('\n').map(x=>x.trim()).filter(Boolean),entityRefs:Object.fromEntries(refs.filter(([,s])=>s.value).map(([key,s])=>[key,Number(s.value)]))};
  // Omit an unchanged old output: backend clears it on a substantive edit.
  if(!shot||output.value!==(v.outputAssetId||''))fields.outputAssetId=output.value||null;
  return storyWrite({action:'shot',id:id.value,fields},revision);
 });
}
function reviewShot(shot){
 const revision=storyRevision,form=storyEditor(`${shot.id} v${shot.version} · 视觉验收`);
 form.append(el('p','muted','请查看实际输出，核对人物、服装、道具、空间与动作衔接；有图不代表通过。'));
 if(shot.outputAssetId){const link=el('a','','打开本版本完整图片');link.href='/media/'+shot.outputAssetId+'/preview?project='+encodeURIComponent(storyProject);link.target='_blank';link.rel='noopener';form.append(link);}
 const status=storySelect(form,'结果',[['fail','需要修改'],['pass','已检查并通过']],'fail');
 const evidence=storyControl(form,'可见结果与检查依据','','textarea');evidence.required=true;
 storySave(form,()=>storyWrite({action:'review',id:shot.id,shotVersion:shot.version,status:status.value,evidence:evidence.value},revision));
}
async function downloadStory(final){
 if(routedProject!==storyProject)throw new Error('项目已切换');
 const data=await api('/api/storyboard-export?project='+encodeURIComponent(storyProject)+'&final='+(final?'1':'0'));
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
 const a=el('a');a.href=url;a.download=`storyboard-${data.projectId}-r${data.revision}-${final?'reviewed':'draft'}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
storyButton.onclick=()=>openStory().catch(e=>toast(e.message));
