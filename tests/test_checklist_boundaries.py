from pathlib import Path
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

SOURCE=Path(os.environ.get('CHECKLIST_SOURCE',Path(__file__).resolve().parents[1]/'disaster/core/knowledge_base_search.py'))

class ChecklistBoundaryTests(unittest.TestCase):
    def indexed(self,text):
        with tempfile.TemporaryDirectory(prefix='checklist-cli-')as temp:
            root=Path(temp);directory=root/'knowledge_base';directory.mkdir();fixture=directory/'fixture.md';fixture.write_text(text)
            result=subprocess.run([sys.executable,str(SOURCE)],cwd=root,text=True,capture_output=True,timeout=10)
            self.assertEqual(result.returncode,0,result.stderr);self.assertIn('Indexed 1 files',result.stdout)
            spec=importlib.util.spec_from_file_location('checklist_subject',SOURCE);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            reopened=module.KnowledgeBaseSearch(str(directory),str(root/'knowledge_base.db'))
            rows=reopened.get_checklists();self.assertEqual(fixture.read_text(),text)
            return {row['title']:[(item['text'],item['checked'])for item in row['items']]for row in rows}

    def test_sibling_heading_closes_but_nested_heading_keeps_items(self):
        text='# Fixture\n## Packing Checklist\n- [ ] Pack fixture\n### Category\n- [x] Pack nested\n## Notes\n- Background only\n'
        self.assertEqual(self.indexed(text),{'Packing Checklist':[('Pack fixture',False),('Pack nested',True)]})

    def test_higher_heading_closes_current_checklist(self):
        text='### Small Checklist\n- [ ] Keep\n## Notes\n- Exclude\n# End\n* Exclude again\n'
        self.assertEqual(self.indexed(text),{'Small Checklist':[('Keep',False)]})

    def test_consecutive_checklists_and_eof_preserve_existing_bullet_forms(self):
        text='## First Checklist\n- [ ] First\n## Second Checklist\n* Plain star\n- Plain dash\n- [x] Done\n- [ ] Last'
        self.assertEqual(self.indexed(text),{'First Checklist':[('First',False)],'Second Checklist':[('Plain star',False),('Plain dash',False),('Done',True),('Last',False)]})

    def test_empty_checklist_stays_omitted_and_plain_document_adds_none(self):
        self.assertEqual(self.indexed('## Empty Checklist\n## Notes\n- Not a task\n'),{})
        self.assertEqual(self.indexed('# Plain\n- Ordinary paragraph bullet\n'),{})

if __name__=='__main__':unittest.main()
