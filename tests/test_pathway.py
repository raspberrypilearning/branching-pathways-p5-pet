"""Check source integrity and learner snippets, including mixed pathway choices."""
import ast
import importlib.util
import itertools
import json
import math
from pathlib import Path
import re
import sys
import types
import unittest
from unittest.mock import patch
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / 'en'
STARTER = (ROOT / 'starters/pet.py').read_text()
FILES = re.findall(r'^        file: (.+)$', (EN / 'pathways.yml').read_text(), re.M)


def snippets():
    result = {}
    for filename in FILES[1:]:
        code = re.findall(r'```python\n(.*?)\n```', (EN / filename).read_text(), re.S)
        if code:
            result[filename.split(' - ')[0]] = code[0]
    return result


def combine(codes):
    tree = ast.parse(STARTER)
    for code in codes:
        replacement = ast.parse(code).body[0]
        assert isinstance(replacement, ast.FunctionDef)
        tree.body = [replacement if isinstance(node, ast.FunctionDef) and node.name == replacement.name else node for node in tree.body]
    return ast.unparse(ast.fix_missing_locations(tree))


def run_pet(source):
    p5 = types.ModuleType('p5')
    p5.dist = lambda x1, y1, x2, y2: math.hypot(x1-x2, y1-y2)
    p5.mouse_x, p5.mouse_y, p5.frame_count = 200, 230, 0
    p5.width, p5.height = 400, 400
    for name in ['size', 'no_stroke', 'background', 'fill', 'rect', 'circle', 'ellipse', 'triangle', 'text_size', 'text', 'run']:
        setattr(p5, name, lambda *args: None)
    namespace = {}
    with patch.dict(sys.modules, {'p5': p5}):
        exec(compile(source, '<learner pet>', 'exec'), namespace)
    namespace['setup']()
    return namespace


class ContentChecks(unittest.TestCase):
    def test_sources_and_metadata_agree(self):
        ids = re.findall(r'^      - id: (\w+)$', (EN / 'pathways.yml').read_text(), re.M)
        self.assertEqual(len(FILES), 18)
        self.assertEqual(len(set(ids)), 18)
        titles = re.findall(r"^  - title: '(.+)'$", (EN / 'meta.yml').read_text(), re.M)
        self.assertEqual(titles, [Path(f).stem for f in FILES])
        flow = (EN / 'step-dependencies.mermaid').read_text()
        for index, (id, filename) in enumerate(zip(ids, FILES), 1):
            text = (EN / filename).read_text()
            self.assertEqual(text, (EN / f'step_{index}.md').read_text())
            self.assertIn('## Test', text)
            self.assertEqual(len(re.findall(rf'P{id}\[', flow)), 1)
            if id != '1A':
                self.assertIn(f'Hub --> P{id}', flow)
                self.assertIn(f'P{id} --> Hub', flow)

    def test_local_links_and_assets_exist(self):
        for path in [EN / 'landing.md', *(EN / name for name in FILES)]:
            for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                if target.startswith(('http://', 'https://')):
                    continue
                self.assertTrue((EN / unquote(target.split('#')[0])).is_file(), (path.name, target))
        for filename in ['assets/pet-maker.svg','assets/pet-icon.svg','en/images/banner.svg']:
            self.assertTrue((ROOT / filename).is_file())

    def test_starter_is_exact_on_setup_page(self):
        source = (EN / FILES[0]).read_text()
        self.assertIn('```python\n'+STARTER.strip()+'\n```', source)
        for filename in ['en/resources/pet.py', 'en/code/p5-pet-starter/main.py']:
            self.assertEqual(STARTER, (ROOT / filename).read_text())

    def test_snippets_are_complete_existing_functions(self):
        names = {n.name for n in ast.parse(STARTER).body if isinstance(n, ast.FunctionDef)}
        for id, code in snippets().items():
            tree = ast.parse(code)
            self.assertEqual(len(tree.body), 1, id)
            self.assertIsInstance(tree.body[0], ast.FunctionDef, id)
            self.assertIn(tree.body[0].name, names, id)

    def test_browser_titles_hide_ids_and_menu_order(self):
        data = json.loads((ROOT / 'data/pages.json').read_text())
        self.assertEqual([g['slug'] for g in data['groups']], ['setup','controls','body','move','personality','home-scene','improve','ideas'])
        for page in data['pages'].values():
            self.assertNotRegex(page['title'], r'^\d+[A-Z]')
        self.assertIn('.callout.caution{background:var(--pink)', (ROOT / 'styles.css').read_text())


class PetBehaviour(unittest.TestCase):
    def test_starter_click_inside_outside_and_toggle(self):
        pet = run_pet(STARTER)
        pet['draw']()
        pet['mouse_x'],pet['mouse_y']=0,0
        pet['mouse_pressed']()
        self.assertEqual(pet['mood'],'calm')
        pet['mouse_x'],pet['mouse_y']=pet['x'],pet['y']
        pet['mouse_pressed']()
        self.assertEqual(pet['mood'],'happy')
        pet['mouse_pressed']()
        self.assertEqual(pet['mood'],'calm')

    def test_each_option_works_directly_from_starter(self):
        for id, code in snippets().items():
            with self.subTest(page=id):
                pet = run_pet(combine([code]))
                for frame in [0,1,30,60,150]:
                    pet['frame_count']=frame
                    pet['draw']()
                pet['mouse_x'],pet['mouse_y']=pet['x'],pet['y']
                pet['mouse_pressed']()
                pet['key_pressed']()
                pet['draw']()

    def test_mixed_routes_keep_control_and_body_working(self):
        options = snippets()
        # 3 bodies × 4 movements × 4 reactions × 3 homes = 144 combinations.
        sets = [[None,'3A','3B'], [None,'4A','4B','4C'], [None,'5A','5B','5C'], [None,'6A','6B']]
        for ids in itertools.product(*sets):
            codes = [options[id] for id in ids if id] + [options['2B'], options['3C']]
            with self.subTest(parts=ids):
                pet = run_pet(combine(codes))
                for frame in [0,30,90,240]:
                    pet['frame_count']=frame
                    pet['draw']()
                    self.assertTrue(65 <= pet['x'] <= 335)
                    self.assertTrue(95 <= pet['y'] <= 275)
                pet['mouse_x'],pet['mouse_y']=pet['x'],pet['y']
                pet['mouse_pressed']()
                pet['key_pressed']()
                pet['draw']()
                self.assertIn(pet['mood'], ['calm','happy','sleepy'])
                self.assertIsInstance(pet['message'],str)

    def test_pointer_stays_within_declared_limits(self):
        pet=run_pet(combine([snippets()['4C']]))
        for pointer, expected in [((-50,-50),(70,100)),((900,900),(330,270)),((200,200),(200,200))]:
            pet['mouse_x'],pet['mouse_y']=pointer
            pet['move_pet']()
            self.assertEqual((pet['x'],pet['y']),expected)


if __name__ == '__main__':
    unittest.main()
