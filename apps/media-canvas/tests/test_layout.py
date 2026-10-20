import copy
import unittest
from unittest.mock import patch
import test_canvas
from layout import arrange, intersects, positions

class LayoutTests(unittest.TestCase):
    setUp=test_canvas.CanvasTests.setUp
    tearDown=test_canvas.CanvasTests.tearDown
    create=test_canvas.CanvasTests.create

    def assert_clear(self,state):
        for i,a in enumerate(state['nodes']):
            for b in state['nodes'][i+1:]:
                self.assertFalse(intersects(a,b,gap=0),(a['id'],b['id']))

    def production_flow(self):
        task=self.create();self.store.update_task(task['id'],'running')
        for i in range(4):
            a=copy.deepcopy(self.asset);a.update(id='a_'+str(i)*20,title='很长的标题'*80)
            with patch.object(self.store,'prepare_asset',return_value=a):
                self.store.import_asset('ignored',task_ref=task['ref'],parent='n1')
        self.store.update_task(task['id'],'review','很长的结果文字'*100)
        return task

    def test_insertions_do_not_overlap_and_content_is_preserved(self):
        self.production_flow()
        self.store.add_note(dict(requestId='note',title='批注',text='保留原图',nodeIds=['n1']))
        before=self.store.read();self.assert_clear(before)
        # Simulate the old crowded board, then restore semantic order.
        self.store.patch_board(dict(positions={n['id']:dict(x=20,y=20) for n in before['nodes']}))
        crowded=self.store.read();self.store.layout(dict(expectedRevision=crowded['revision']))
        after=self.store.read();self.assert_clear(after)
        for key in ['assets','tasks','notes','edges','annotations']:
            self.assertEqual(before[key],after[key])
        nodes=after['nodes'];task=next(n for n in nodes if n['kind']=='task');result=next(n for n in nodes if n['kind']=='result')
        outputs=[n for n in nodes if n.get('assetId') in after['tasks'][0]['outputAssetIds']]
        self.assertLess(nodes[0]['x'],task['x'])
        self.assertTrue(all(task['x']<n['x']<result['x'] for n in outputs))
        self.assertEqual([n['y'] for n in outputs],sorted(n['y'] for n in outputs))
        self.assertEqual(arrange(after),positions(after))

    def test_undo_revision_and_intervening_drag_guards(self):
        self.production_flow();before=self.store.read()
        self.store.layout(dict(expectedRevision=before['revision']))
        arranged=self.store.read()
        with self.assertRaises(ValueError):self.store.layout(dict(expectedRevision=before['revision'],action='undo'))
        self.store.layout(dict(expectedRevision=arranged['revision'],action='undo'))
        self.assertEqual(positions(self.store.read()),positions(before))
        self.store.layout(dict(expectedRevision=self.store.read()['revision']))
        self.store.patch_board(dict(positions={'n1':dict(x=123,y=456)}))
        changed=self.store.read()
        with self.assertRaises(ValueError):self.store.layout(dict(expectedRevision=changed['revision'],action='undo'))
        self.assertEqual(changed,self.store.read())

    def test_cycles_empty_and_new_nodes_are_safe(self):
        s=dict(nodes=[],edges=[],tasks=[],assets=[]);self.assertEqual(arrange(s),{})
        s['nodes']=[dict(id='a',kind='note',x=0,y=0),dict(id='b',kind='note',x=0,y=0)]
        s['edges']=[dict(source='a',target='b'),dict(source='b',target='a')]
        a=arrange(s);self.assertEqual(set(a),{'a','b'});self.assertNotEqual(a['a'],a['b'])
        self.create();self.store.layout(dict(expectedRevision=self.store.read()['revision']))
        self.store.add_note(dict(requestId='extra',title='新',text='新增',nodeIds=[]))
        with self.assertRaises(ValueError):self.store.layout(dict(expectedRevision=self.store.read()['revision'],action='undo'))

if __name__=='__main__':unittest.main()
