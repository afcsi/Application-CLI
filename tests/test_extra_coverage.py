import os
import sys
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from datetime import date, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import task_manager as tm  # noqa: E402


class TestExtraCoverage(unittest.TestCase):
    def setUp(self):
        # tasks.json isolé par test
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        tm.TASKS_FILE = self.tmp.name

    def tearDown(self):
        try:
            os.remove(self.tmp.name)
        except OSError:
            pass

    def run_cli(self, argv):
        saved_argv = sys.argv
        sys.argv = ['prog'] + argv
        buf = StringIO()
        try:
            with redirect_stdout(buf):
                tm.main()
        finally:
            sys.argv = saved_argv
        return buf.getvalue()

    def test_cli_help_when_no_args(self):
        # Couvre la branche: aucun sous-commande -> parser.print_help()
        out = self.run_cli([])
        self.assertIn("Gestionnaire de tâches CLI", out)

    def test_list_sort_date_handles_missing_due(self):
        # Couvre key_date() quand due est vide (-> date.max)
        today = date.today().strftime("%Y-%m-%d")
        tasks = [
            {'id': 1, 'title': 'A', 'desc': '', 'priority': 2, 'due': today, 'created': ''},
            {'id': 2, 'title': 'B', 'desc': '', 'priority': 1, 'due': '',    'created': ''},  # due vide
        ]
        with open(self.tmp.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        class Args: pass
        args = Args()
        args.sort = 'date'
        args.overdue = False
        args.due_in = None

        buf = StringIO()
        saved = sys.stdout
        sys.stdout = buf
        tm.list_tasks(args)
        sys.stdout = saved

        out = buf.getvalue().strip().splitlines()
        # La tâche avec vraie date (id 1) doit apparaître avant celle avec due vide (id 2)
        self.assertTrue(out[0].startswith("[1]"))
        self.assertTrue(out[1].startswith("[2]"))

    def test_status_flag_soon_is_printed(self):
        # Couvre le chemin "⏳ soon" (échéance <= 3 jours)
        soon = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        tasks = [{'id': 1, 'title': 'Soon', 'desc': '', 'priority': 3, 'due': soon, 'created': ''}]
        with open(self.tmp.name, 'w', encoding='utf-8') as f:
            json.dump(tasks, f)

        class Args: pass
        args = Args()
        args.sort = 'date'
        args.overdue = False
        args.due_in = None

        buf = StringIO()
        saved = sys.stdout
        sys.stdout = buf
        tm.list_tasks(args)
        sys.stdout = saved

        self.assertIn("⏳", buf.getvalue())  # l’indicateur doit apparaître


if __name__ == "__main__":
    unittest.main()
