import os
import sys
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from datetime import date

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import task_manager as tm  # noqa: E402


class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.tmpfile = tempfile.NamedTemporaryFile(delete=False)
        self.tmpfile.close()
        tm.TASKS_FILE = self.tmpfile.name

    def tearDown(self):
        try:
            os.remove(self.tmpfile.name)
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

    def test_full_cli_flow_add_list_delete(self):
        today = date.today().strftime("%Y-%m-%d")

        # add
        out = self.run_cli([
            'add', '--title', 'T', '--desc', 'D', '--priority', '1', '--due', today
        ])
        self.assertIn("Tâche ajoutée", out)

        # list (priority)
        out = self.run_cli(['list', '--sort', 'priority'])
        self.assertIn("[1] T (Priorité: 1 – Due: " + today + ")", out)

        # edit
        out = self.run_cli(['edit', '--id', '1', '--priority', '2'])
        self.assertIn("mise à jour", out)

        # delete
        out = self.run_cli(['delete', '--id', '1'])
        self.assertIn("Tâche 1 supprimée", out)

        # list vide
        out = self.run_cli(['list'])
        self.assertIn("Aucune tâche à afficher.", out)


if __name__ == '__main__':
    unittest.main()
