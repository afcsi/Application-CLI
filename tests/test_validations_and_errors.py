import os
import sys
import json
import tempfile
import unittest
from io import StringIO
from datetime import date, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import task_manager as tm  # noqa: E402


class TestValidationsAndErrors(unittest.TestCase):
    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile(delete=False)
        self.tmpfile.close()
        tm.TASKS_FILE = self.tmpfile.name

    def tearDown(self):
        try:
            os.remove(self.tmpfile.name)
        except OSError:
            pass

    def test_validate_priority_raises(self):
        with self.assertRaises(ValueError):
            tm.validate_priority(0)
        with self.assertRaises(ValueError):
            tm.validate_priority(6)

    def test_validate_due_raises(self):
        with self.assertRaises(ValueError):
            tm.validate_due("20-01-2025")
        with self.assertRaises(ValueError):
            tm.validate_due("not-a-date")

    def test_delete_nonexistent_id_message(self):
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump([{'id': 1, 'title': 'A', 'desc': '', 'priority': 1,
                        'due': date.today().strftime("%Y-%m-%d"), 'created': ''}], f)

        class Args: pass
        args = Args(); args.id = 999

        saved = sys.stdout; out = StringIO(); sys.stdout = out
        tm.delete_task(args)
        sys.stdout = saved

        self.assertIn("Aucune tâche trouvée", out.getvalue())

    def test_edit_nonexistent_id_message(self):
        with open(self.tmpfile.name, 'w', encoding='utf-8') as f:
            json.dump([], f)

        class Args: pass
        args = Args(); args.id = 1; args.title = "X"; args.desc = None
        args.priority = None; args.due = None

        saved = sys.stdout; out = StringIO(); sys.stdout = out
        tm.edit_task(args)
        sys.stdout = saved

        self.assertIn("Aucune tâche trouvée", out.getvalue())


if __name__ == '__main__':
    unittest.main()
