import os
import sys
import json
import tempfile
import unittest
from io import StringIO

# Permet d'importer le module src/task_manager.py en local et en CI
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import task_manager as tm


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Fichier temporaire pour simuler tasks.json
        self.tmpfile = tempfile.NamedTemporaryFile(delete=False)
        self.tmpfile.close()  # important pour Windows/CI
        tm.TASKS_FILE = self.tmpfile.name

    def tearDown(self):
        try:
            os.remove(self.tmpfile.name)
        except OSError:
            pass

    def test_add_and_load_task(self):
        class Args:
            pass
        args = Args()
        args.title = "Test"
        args.desc = "Desc"
        args.priority = 2
        args.due = "2025-12-31"
        tm.add_task(args)

        with open(self.tmpfile.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        task = data[0]
        self.assertEqual(task['title'], "Test")
        self.assertEqual(task['priority'], 2)
        self.assertEqual(task['due'], "2025-12-31")
        self.assertIn('id', task)

    def test_list_tasks_empty(self):
        saved = sys.stdout
        out = StringIO()
        sys.stdout = out

        class Args:
            pass
        args = Args()
        args.sort = 'priority'
        tm.list_tasks(args)
        output = out.getvalue().strip()

        sys.stdout = saved
        self.assertIn("Aucune tâche à afficher.", output)

    def test_delete_task(self):
        tasks = [
            {'id': 1, 'title': 'T1', 'desc': '', 'priority': 1, 'due': '2025-01-01', 'created': ''},
            {'id': 2, 'title': 'T2', 'desc': '', 'priority': 2, 'due': '2025-02-01', 'created': ''}
        ]
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        class Args:
            pass
        args = Args()
        args.id = 1

        saved = sys.stdout
        out = StringIO()
        sys.stdout = out

        tm.delete_task(args)

        sys.stdout = saved
        output = out.getvalue().strip()
        self.assertIn("Tâche 1 supprimée.", output)

        with open(self.tmpfile.name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 2)


if __name__ == '__main__':
    unittest.main()
