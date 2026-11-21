"""Whole API/auth/init request tests, temporary fixture profiles and no network."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(os.environ.get('PREPAREDNESS_SOURCE', Path(__file__).resolve().parents[1]))
PROGRAM = '''
import os,sys,json,hashlib,socket
from pathlib import Path
root=Path.cwd()
marker='synthetic-fixture-not-a-real-credential'
other='second-synthetic-fixture-not-a-real-credential'
config={'api_keys':{}}
for label,key,user,profile in [('one',marker,'fixture-user','default'),('two',other,'other-user','secondary')]:
 config['api_keys'][label]={'key_hash':hashlib.sha256(key.encode()).hexdigest(),'user_id':user,'role':'user','profile':profile,'permissions':['read','write']}
p=root/'fixture-api.json';p.write_text(json.dumps(config))
os.environ['EMERGENCY_API_KEYS_FILE']=str(p)
os.environ['EMERGENCY_API_SECRET_KEY']='synthetic-local-signing-fixture-not-a-real-secret-123'
sys.path.insert(0,str(Path(sys.argv[1])/'disaster'))
attempts=[]
def blocked(*a,**k):
 attempts.append(1)
 raise AssertionError('Network prohibited')
socket.socket.connect=blocked
socket.create_connection=blocked
import api_server
from fastapi.testclient import TestClient
from user_profile_manager import UserProfileManager
headers={'Authorization':'Bearer '+marker}
with TestClient(api_server.app)as client:
 def put(payload,h=headers):
  r=client.put('/api/profile',headers=h,json=payload)
  assert r.status_code==200,r.text
  return r.json()
 def get(h=headers):
  r=client.get('/api/profile',headers=h);assert r.status_code==200,r.text
  return r.json()['profile']
 case=sys.argv[2]
 if case=='fresh-corrections':
  for family,location,preferences in [({'adults':2,'children':0},{'type':'urban'},{'fixture_option':'old'}),({'adults':3,'children':1},{'type':'rural'},{'fixture_option':'new'})]:
   result=put(dict(family=family,location=location,preferences=preferences))
   assert result['success']and result['sections_updated']==3,result
  actual=get();disk=json.loads((root/'preparedness_data/profiles/default.json').read_text())
  reopened=UserProfileManager('preparedness_data');reopened.load_profile('default')
  for record in [actual,disk,reopened.profile_data]:
   assert record['family']['adults']==3 and record['family']['children']==1,record
   assert record['location']['type']=='rural'and record['preferences']['fixture_option']=='new',record
 elif case=='partial-and-empty':
  assert put({'family':{'adults':2,'children':0},'location':{'type':'urban'}})['sections_updated']==2
  result=put({'family':{'children':1}});assert result['sections_updated']==1,result
  actual=get();assert actual['family']['adults']==2 and actual['family']['children']==1,actual
  assert actual['location']['type']=='urban',actual
  before=actual
  assert put({})['sections_updated']==0
  after=get();assert after==before,(before,after)
 elif case=='profile-scope':
  h2={'Authorization':'Bearer '+other}
  assert put({'family':{'adults':2}})['success']
  assert put({'family':{'adults':4}},h2)['success']
  assert put({'family':{'adults':3}})['success']
  assert get()['family']['adults']==3
  assert get(h2)['family']['adults']==4
  assert json.loads((root/'preparedness_data/profiles/default.json').read_text())['family']['adults']==3
  assert json.loads((root/'preparedness_data/profiles/secondary.json').read_text())['family']['adults']==4
 elif case=='automatic-cache':
  assert put({'family':{'adults':2},'location':{'type':'urban'},'preferences':{'fixture_option':'kept'}})['success']
  manager=api_server.systems['fixture-user'].profile_manager
  assert manager.is_update_needed('family')is False
  assert manager.save_family_info({'adults':99})is False
  assert manager.save_location_info({'type':'not-saved'})is False
  assert manager.save_preferences({'fixture_option':'not-saved'})is False
  actual=get();assert actual['family']['adults']==2 and actual['location']['type']=='urban'
  assert actual['preferences']['fixture_option']=='kept'
 else:raise AssertionError(case)
assert not attempts,attempts
print('FIXTURE_PROFILE_RESULT='+json.dumps({'case':case,'network_attempts':len(attempts)}))
'''


class ExplicitProfilePUT(unittest.TestCase):
    def check_case(self, case):
        with tempfile.TemporaryDirectory(prefix='preparedness-profile-put-') as temp:
            env = dict(os.environ, HOME=temp, XDG_CONFIG_HOME=temp,
                       MPLBACKEND='Agg', MPLCONFIGDIR=str(Path(temp) / 'mpl'),
                       PYTHONDONTWRITEBYTECODE='1')
            result = subprocess.run([sys.executable, '-c', PROGRAM, str(ROOT), case],
                                    cwd=temp, env=env, capture_output=True,
                                    text=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + '\n' + result.stderr)
            self.assertIn('"network_attempts": 0', result.stdout)

    def test_fresh_explicit_corrections_persist_all_sections(self):
        self.check_case('fresh-corrections')

    def test_partial_and_empty_updates_preserve_unspecified_values(self):
        self.check_case('partial-and-empty')

    def test_authenticated_profile_scope_stays_separate(self):
        self.check_case('profile-scope')

    def test_automatic_helpers_keep_existing_freshness_gate(self):
        self.check_case('automatic-cache')
