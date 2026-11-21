"""Actual complete root CLI expiry checks, temporary synthetic inventory only."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(os.environ.get('PREPAREDNESS_SOURCE', Path(__file__).resolve().parents[1]))
SCRIPT = ROOT / 'disaster' / 'integrated_preparedness_system.py'
spec = importlib.util.spec_from_file_location('fixture_supply_tracker', ROOT / 'disaster/core/supply_inventory_tracker.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
BOOTSTRAP = '''import runpy,sys,socket,os
attempts=[]
def blocked(*a,**k):
 attempts.append(1)
 raise AssertionError("Network forbidden")
socket.socket.connect=blocked
socket.create_connection=blocked
sys.argv=sys.argv[1:]
sys.path.insert(0,os.path.dirname(os.path.abspath(sys.argv[0])))
try:runpy.run_path(sys.argv[0],run_name="__main__")
finally:print("FIXTURE_NETWORK_ATTEMPTS="+str(len(attempts)),file=sys.stderr)
'''


class ExpiryCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='preparedness-expiry-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'preparedness_data').mkdir()
        self.tracker = module.SupplyInventoryTracker(str(self.root / 'preparedness_data/supplies.db'))

    def run_cli(self, interactive=False):
        env = dict(os.environ, HOME=str(self.root), XDG_CONFIG_HOME=str(self.root),
                   PYTHONDONTWRITEBYTECODE='1', MPLBACKEND='Agg',
                   MPLCONFIGDIR=str(self.root / 'mpl'))
        command = [sys.executable, '-c', BOOTSTRAP, str(SCRIPT), '--supplies']
        if not interactive: command.append('--check-expiry')
        result = subprocess.run(command, cwd=self.root, env=env,
                                input='4\n30\n0\n' if interactive else None,
                                text=True, capture_output=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('FIXTURE_NETWORK_ATTEMPTS=0', result.stderr)
        return result.stdout

    def populate(self):
        for name, quantity, date in [
            ('Synthetic expired fixture', 4, '2000-01-01'),
            ('Synthetic future fixture', 4, '2999-12-31'),
            ('Synthetic undated fixture', 4, None),
            ('Synthetic zero quantity fixture', 0, '2000-01-01')
        ]:
            self.tracker.add_supply('food', name, quantity, 'calories', date, 'synthetic')

    def test_empty_flags_reports_no_items(self):
        self.assertIn('No items expiring soon', self.run_cli())

    def test_populated_flags_agrees_with_public_tracker_identity_and_expiration(self):
        self.populate()
        expected = self.tracker.check_expiration_alerts(30)
        self.assertEqual(len(expected), 1)
        text = self.run_cli()
        for item in expected:
            self.assertIn(f"{item['item']}: expires {item['expiration']}", text)
        for excluded in ['future fixture', 'undated fixture', 'zero quantity fixture']:
            self.assertNotIn(excluded, text)

    def test_existing_interactive_thirty_day_route_remains_valid(self):
        self.populate()
        text = self.run_cli(interactive=True)
        for item in self.tracker.check_expiration_alerts(30):
            self.assertIn(f"{item['item']}: expires in {item['days_until']} days", text)
