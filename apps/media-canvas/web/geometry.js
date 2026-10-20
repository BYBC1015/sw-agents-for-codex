(function(root){
 'use strict';
 const width=250,gap=24,height=n=>n.kind==='asset'?252:190;
 const overlaps=(a,b,padding=gap)=>a.x<b.x+width+padding&&a.x+width+padding>b.x&&a.y<b.y+height(b)+padding&&a.y+height(a)+padding>b.y;
 function settle(nodes,ids){
  const moved=nodes.filter(n=>ids.has(n.id)),fixed=nodes.filter(n=>!ids.has(n.id));
  const clear=(dx,dy)=>moved.every(n=>fixed.every(o=>!overlaps({...n,x:n.x+dx,y:n.y+dy},o)));
  if(!moved.length||clear(0,0))return {dx:0,dy:0};
  const shifts=[];
  for(const n of moved)for(const o of fixed){
   shifts.push({dx:o.x+width+gap-n.x,dy:0},{dx:o.x-width-gap-n.x,dy:0},
    {dx:0,dy:o.y+height(o)+gap-n.y},{dx:0,dy:o.y-height(n)-gap-n.y});
  }
  shifts.sort((a,b)=>(a.dx*a.dx+a.dy*a.dy)-(b.dx*b.dx+b.dy*b.dy)||a.dy-b.dy||a.dx-b.dx);
  const shift=shifts.find(p=>clear(p.dx,p.dy));
  if(shift)for(const n of moved){n.x+=shift.dx;n.y+=shift.dy;}
  return shift||{dx:0,dy:0};
 }
 const api={width,height,overlaps,settle};
 if(typeof module!=='undefined')module.exports=api;else root.CanvasGeometry=api;
})(typeof globalThis==='object'?globalThis:this);
