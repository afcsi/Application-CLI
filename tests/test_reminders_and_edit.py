import os
import sys
import json
import tempfile
import unittest
from io import StringIO
from datetime import date, timedelta

# Import du code depuis src/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import task_manager as tm  # noqa: E402


class TestRemindersAndEdit(unittest.TestCase):
    def setUp(self):
        # Fichier temporaire pour isoler tasks.json à chaque test
        self.tmpfile = tempfile.NamedTemporaryFile(delete=False)
        self.tmpfile.close()
        tm.TASKS_FILE = self.tmpfile.name

    def tearDown(self):
        try:
            os.remove(self.tmpfile.name)
        except OSError:
            pass

    # Helper date → "YYYY-MM-DD"
    def d(self, delta_days: int) -> str:
        return (date.today() + timedelta(days=delta_days)).strftime("%Y-%m-%d")

    def test_edit_task_updates_selected_fields(self):
        # Prépare une tâche
        tasks = [{
            'id': 1, 'title': 'A', 'desc': 'x', 'priority': 3,
            'due': self.d(5), 'created': ''
        }]
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        # Modifie titre, priorité, due (desc laissée intacte)
        class Args:  # args simulés
            pass
        args = Args()
        args.id = 1
        args.title = "B"
        args.desc = None
        args.priority = 1
        args.due = self.d(7)

        tm.edit_task(args)

        with open(self.tmpfile.name, 'r', encoding='utf-8') as f:
            data = json.load(f)

        t = data[0]
        self.assertEqual(t['title'], "B")
        self.assertEqual(t['priority'], 1)
        self.assertEqual(t['due'], self.d(7))
        self.assertEqual(t['desc'], 'x')  # inchangé

    def test_list_overdue_filter(self):
        # 1 tâche en retard, 1 future
        tasks = [
            {'id': 1, 'title': 'old',  'desc': '', 'priority': 2, 'due': self.d(-1), 'created': ''},
            {'id': 2, 'title': 'soon', 'desc': '', 'priority': 2, 'due': self.d(2),  'created': ''},
        ]
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        class Args:
            pass
        args = Args()
        args.sort = 'date'
        args.overdue = True
        args.due_in = None

        saved = sys.stdout
        out = StringIO()
        sys.stdout = out
        tm.list_tasks(args)
        sys.stdout = saved

        output = out.getvalue()
        self.assertIn("[1]", output)
        self.assertNotIn("[2]", output)

    def test_list_due_in_filter(self):
        # 1 proche (≤ 3 jours), 1 lointaine
        tasks = [
            {'id': 1, 'title': 'far',  'desc': '', 'priority': 2, 'due': self.d(5), 'created': ''},
            {'id': 2, 'title': 'near', 'desc': '', 'priority': 2, 'due': self.d(2), 'created': ''},
        ]
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        class Args:
            pass
        args = Args()
        args.sort = 'date'
        args.overdue = False
        args.due_in = 3

        saved = sys.stdout
        out = StringIO()
        sys.stdout = out
        tm.list_tasks(args)
        sys.stdout = saved

        output = out.getvalue()
        self.assertIn("[2]", output)
        self.assertNotIn("[1]", output)


if __name__ == '__main__':
    unittest.main()
