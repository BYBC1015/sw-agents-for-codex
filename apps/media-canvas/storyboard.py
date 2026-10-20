"""Versioned shots and explicit continuity dependencies. Never generates media."""
import copy
import math
import re
from bridge import bounded_text, page


def board(state):
    return state.setdefault('storyboard', {'entities': [], 'shots': []})


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', value):
        raise ValueError('编号须为1–80位字母、数字、下划线或短横线')
    return value


def find(items, key):
    result = next((item for item in items if item['id'] == key), None)
    if result is None:
        raise ValueError('对象不存在于此项目：' + str(key))
    return result


def current(item):
    return version(item, item['currentVersion'])


def version(item, number):
    if type(number) is not int:
        raise ValueError('版本号须为整数')
    value = next((v for v in item['versions'] if v['version'] == number), None)
    if value is None:
        raise ValueError('版本不存在')
    return value


def locks(value):
    if not isinstance(value, list) or len(value) > 40:
        raise ValueError('锁定项须为列表，最多40条')
    return list(dict.fromkeys(bounded_text(v, '锁定项', 1000, True) for v in value))


def check_asset(state, asset_id):
    if asset_id is not None:
        find(state['assets'], asset_id)
    return asset_id


def issues(state, shot):
    s = current(shot)
    result = []
    for entity_id, used in s['entityRefs'].items():
        latest = find(board(state)['entities'], entity_id)['currentVersion']
        if latest != used:
            result.append(dict(type='dependency', entityId=entity_id, usedVersion=used, currentVersion=latest))
    if not s.get('outputAssetId'):
        result.append(dict(type='missing-output'))
    review = s.get('reviews', [])
    if not review or review[-1]['status'] != 'pass':
        result.append(dict(type='visual-review', status=review[-1]['status'] if review else 'unchecked'))
    return result


def shot_view(state, shot):
    return dict(id=shot['id'], **copy.deepcopy(current(shot)),
                availableVersions=[v['version'] for v in shot['versions']], issues=issues(state, shot))


class StoryboardFlow:
    def storyboard_read(self, kind='shots', offset=0, limit=12):
        state = self.read()
        if kind not in ('shots', 'entities'):
            raise ValueError('请选择 shots 或 entities')
        data = board(state)
        items = ([shot_view(state, s) for s in data['shots']] if kind == 'shots' else
                 [dict(id=e['id'], kind=e['kind'], **copy.deepcopy(current(e)),
                       availableVersions=[v['version'] for v in e['versions']]) for e in data['entities']])
        return dict(projectId=state['projectId'], revision=state['revision'], **page(items, offset, limit))

    def storyboard_impact(self, entity_id):
        state = self.read()
        entity = find(board(state)['entities'], entity_id)
        affected = [dict(shotId=s['id'], shotVersion=s['currentVersion'],
                         usedVersion=current(s)['entityRefs'][entity_id])
                    for s in board(state)['shots'] if entity_id in current(s)['entityRefs']]
        return dict(projectId=state['projectId'], revision=state['revision'], entityId=entity_id,
                    currentVersion=entity['currentVersion'], affectedShots=affected, mediaExecuted=False)

    def shot_packet(self, shot_id):
        state = self.read()
        shot = find(board(state)['shots'], shot_id)
        s = current(shot)
        references = []
        protected = list(s['locks'])
        for key, number in s['entityRefs'].items():
            entity = find(board(state)['entities'], key)
            ref = version(entity, number)
            protected.extend(ref['locks'])
            references.append(dict(entityId=key, kind=entity['kind'], version=number,
                                   description=ref['description'], assetId=ref.get('assetId')))
        return dict(projectId=state['projectId'], revision=state['revision'], shotId=shot_id,
                    shotVersion=s['version'], script=s['script'], camera=s['camera'],
                    references=references, locks=list(dict.fromkeys(protected)),
                    issues=issues(state, shot), mediaExecuted=False)

    def storyboard_export(self, final=False):
        state = self.read()
        shots = [shot_view(state, s) for s in board(state)['shots']]
        ready = bool(shots) and not any(s['issues'] for s in shots)
        if final and not ready:
            raise ValueError('仍有镜头缺图、依赖版本变化或尚未通过视觉验收；可先导出草稿')
        refs = {(key, number) for s in shots for key, number in s['entityRefs'].items()}
        entities = [dict(id=key, kind=find(board(state)['entities'], key)['kind'],
                         **copy.deepcopy(version(find(board(state)['entities'], key), number)))
                    for key, number in sorted(refs)]
        return dict(schemaVersion=1, projectId=state['projectId'], revision=state['revision'],
                    ready=ready, shots=shots, entities=entities,
                    totalDuration=sum(s['duration'] for s in shots), imagesIncluded=False)

    def storyboard_write(self, body):
        def update(state):
            if body.get('expectedRevision') != state['revision']:
                raise ValueError('项目已变化，请重新读取后保存分镜')
            data = board(state)
            action = body.get('action')
            key = identifier(body.get('id'))
            from store import now
            if action in ('entity', 'shot'):
                fields = body.get('fields')
                if not isinstance(fields, dict) or not fields:
                    raise ValueError('请提供修改字段')
                collection = data['entities' if action == 'entity' else 'shots']
                item = next((v for v in collection if v['id'] == key), None)
                old = copy.deepcopy(current(item)) if item else {}
                if action == 'entity':
                    allowed = {'description', 'locks', 'assetId'}
                    kind = item['kind'] if item else body.get('kind')
                    if kind not in ('character', 'wardrobe', 'scene', 'prop', 'product', 'style'):
                        raise ValueError('资产类型不正确')
                    value = dict(description=old.get('description', ''), locks=old.get('locks', []),
                                 assetId=old.get('assetId'))
                else:
                    allowed = {'title', 'script', 'duration', 'camera', 'entityRefs', 'locks', 'outputAssetId'}
                    value = dict(title=old.get('title', key), script=old.get('script', ''),
                                 duration=old.get('duration', 5), camera=old.get('camera', ''),
                                 entityRefs=old.get('entityRefs', {}), locks=old.get('locks', []),
                                 outputAssetId=old.get('outputAssetId'))
                if set(fields) - allowed:
                    raise ValueError('存在不支持的修改字段')
                value.update(copy.deepcopy(fields))
                for name in ('description', 'title', 'script', 'camera'):
                    if name in value:
                        value[name] = bounded_text(value[name], name, 4000, name in ('title', 'description'))
                value['locks'] = locks(value['locks'])
                if action == 'entity':
                    check_asset(state, value['assetId'])
                else:
                    duration = value['duration']
                    if type(duration) not in (int, float) or not math.isfinite(duration) or not 0 < duration <= 3600:
                        raise ValueError('时长须为0–3600秒之间的正数')
                    if not isinstance(value['entityRefs'], dict) or len(value['entityRefs']) > 40:
                        raise ValueError('镜头资产引用须为对象，最多40项')
                    for ref, number in value['entityRefs'].items():
                        version(find(data['entities'], ref), number)
                    # Changing shot intent invalidates its old image and all prior visual approval.
                    changed = old and any(value[f] != old.get(f) for f in ('script', 'camera', 'entityRefs', 'locks'))
                    if changed and 'outputAssetId' not in fields:
                        value['outputAssetId'] = None
                    check_asset(state, value['outputAssetId'])
                    value['reviews'] = []
                number = max((v['version'] for v in item['versions']), default=0) + 1 if item else 1
                value.update(version=number, createdAt=now())
                if not item:
                    item = dict(id=key, currentVersion=number, versions=[])
                    if action == 'entity':
                        item['kind'] = kind
                    collection.append(item)
                item['versions'].append(value)
                item['currentVersion'] = number
            elif action == 'select':
                kind = body.get('kind')
                if kind not in ('shot', 'entity'):
                    raise ValueError('请选择 shot 或 entity')
                item = find(data['shots' if kind == 'shot' else 'entities'], key)
                version(item, body.get('version'))
                item['currentVersion'] = body['version']
            elif action == 'review':
                item = find(data['shots'], key)
                value = current(item)
                if body.get('shotVersion') != item['currentVersion']:
                    raise ValueError('镜头版本已变化，请重新查看图片')
                status = body.get('status')
                if status not in ('pass', 'fail'):
                    raise ValueError('验收状态须为 pass 或 fail')
                evidence = bounded_text(body.get('evidence'), '可见结果的验收依据', 4000, True)
                if status == 'pass' and any(i['type'] != 'visual-review' for i in issues(state, item)):
                    raise ValueError('请先解决缺图和依赖版本变化，再验收')
                value.setdefault('reviews', []).append(dict(status=status, evidence=evidence, createdAt=now()))
            else:
                raise ValueError('不支持的分镜操作')
            return dict(id=key, version=item['currentVersion'], mediaExecuted=False)
        return self._operation('storyboard', body, update)
