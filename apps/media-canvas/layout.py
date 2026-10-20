"""Deterministic flow layout and collision-free placement; media stays untouched."""
WIDTH=250
GAP=48

def height(node):
    return 252 if node['kind']=='asset' else 190

def intersects(a,b,gap=GAP):
    return a['x']<b['x']+WIDTH+gap and a['x']+WIDTH+gap>b['x'] and a['y']<b['y']+height(b)+gap and a['y']+height(a)+gap>b['y']

def place(nodes,node,x=40,y=40):
    candidate=dict(node,x=x,y=y)
    # Advance past complete occupied rectangles, not approximate title coordinates.
    while True:
        hits=[n for n in nodes if n['id']!=node['id'] and intersects(candidate,n)]
        if not hits: return dict(x=candidate['x'],y=candidate['y'])
        candidate['y']=max(n['y']+height(n)+GAP for n in hits)

def arrange(state):
    nodes=state['nodes'];by_id={n['id']:n for n in nodes}
    parents={n['id']:set() for n in nodes}
    for e in state['edges']:
        if e['source'] in by_id and e['target'] in by_id and e['source']!=e['target']:
            parents[e['target']].add(e['source'])
    # A written result follows its generated media, even though both link from the task.
    for n in nodes:
        if n['kind']=='result':
            task=next((t for t in state['tasks'] if t['id']==n['resultTaskId']),None)
            if task:
                parents[n['id']].update(v['id'] for v in nodes if v.get('assetId') in task.get('outputAssetIds',[]) and v['id']!=n['id'])
    ranks={};remaining=set(by_id)
    while remaining:
        ready=[n['id'] for n in nodes if n['id'] in remaining and not (parents[n['id']] & remaining)]
        if not ready:ready=[next(n['id'] for n in nodes if n['id'] in remaining)] # cycles stay usable
        for key in ready:
            ranks[key]=max((ranks[p]+1 for p in parents[key] if p in ranks),default=0)
            remaining.remove(key)
    assets={a['id']:a for a in state['assets']};order={n['id']:i for i,n in enumerate(nodes)}
    result={}
    for rank in sorted(set(ranks.values())):
        group=[n for n in nodes if ranks[n['id']]==rank]
        group.sort(key=lambda n:(assets.get(n.get('assetId'),{}).get('lineage',''),assets.get(n.get('assetId'),{}).get('version',0),order[n['id']]))
        y=40
        for n in group:
            result[n['id']]=dict(x=40+rank*330,y=y);y+=height(n)+GAP
    return result

def positions(state):
    return {n['id']:dict(x=n['x'],y=n['y']) for n in state['nodes']}

def apply_layout(state,body):
    if body.get('expectedRevision')!=state['revision']:raise ValueError('画布已变化，请重试排布')
    before=positions(state)
    if body.get('action','arrange')=='undo':
        undo=state.get('layoutUndo')
        if not undo or before!=undo['after']:raise ValueError('节点位置或数量已变化，无法撤销上次排布')
        target=undo['before'];state.pop('layoutUndo',None)
    elif body.get('action','arrange')=='arrange':
        target=arrange(state)
        if target!=before:state['layoutUndo']=dict(before=before,after=target)
    else:raise ValueError('不支持的排布操作')
    for n in state['nodes']:n.update(target[n['id']])
    return dict(nodeCount=len(target),action=body.get('action','arrange'))
