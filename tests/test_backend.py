import io,json,tempfile,unittest
from pathlib import Path
from datetime import datetime,timezone
from cryptography.fernet import Fernet
from backend.service import Service,Problem,DAY,advance_month
from backend.server import App
class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.now=1769853600;self.s=Service(Path(self.tmp.name)/'db.sqlite3',Fernet.generate_key(),lambda:self.now)
        self.s.seed_districts([('GU2',51.24,-.59),('GU1',51.24,-.56),('SW1A',51.50,-.14)])
        self.a=self.register('alice','GU2');self.b=self.register('bob','GU1');self.c=self.register('carol','SW1A')
    def tearDown(self):self.tmp.cleanup()
    def register(self,name,district):return self.s.register(dict(login=name,password='A-long-test-passphrase',alias=name.title(),bio='Invented test adult',wants='A test conversation',district=district,age_range='40s',adult=True,consent=True))
    def problem(self,status,fn,*args):
        with self.assertRaises(Problem) as c:fn(*args)
        self.assertEqual(c.exception.status,status)
    def conversation(self):
        cid=self.s.request(self.a['user_id'],self.b['user_id'])['id'];self.s.accept(self.b['user_id'],cid);return cid
    def test_two_adults_find_accept_and_exchange_privately(self):
        a,b=self.a['user_id'],self.b['user_id'];found=self.s.discover(a,'GU2',10)
        self.assertEqual([p['id'] for p in found],[b]);self.assertNotIn('login',found[0]);self.assertFalse(found[0]['identity_verified'])
        cid=self.s.request(a,b)['id'];self.problem(403,self.s.send,a,cid,'Not accepted');self.problem(403,self.s.accept,a,cid);self.s.accept(b,cid)
        mid=self.s.send(a,cid,'Hello from Alice')['id'];self.assertEqual(self.s.messages(b,cid)[0]['body'],'Hello from Alice');self.s.send(b,cid,'Hello back');self.assertEqual(len(self.s.messages(a,cid)),2)
        self.problem(404,self.s.messages,self.c['user_id'],cid);self.problem(404,self.s.keep,self.c['user_id'],mid)
        with self.s.db() as db:self.assertNotIn(b'Hello from Alice',db.execute('SELECT body FROM messages WHERE id=?',(mid,)).fetchone()[0])
    def test_recovery_revokes_sessions_and_rotates_code(self):
        token,session=self.s.login('alice','A-long-test-passphrase');self.problem(403,self.s.authenticate,token,'wrong',True)
        self.assertEqual(self.s.authenticate(token,session['csrf'],True),self.a['user_id'])
        self.s.recover('alice',self.a['recovery_code'],'A-new-test-passphrase');self.problem(401,self.s.authenticate,token)
        self.problem(401,self.s.recover,'alice',self.a['recovery_code'],'Another-test-passphrase');self.s.login('alice','A-new-test-passphrase')
    def test_expiry_and_individual_keepsake_visibility(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];mid=self.s.send(a,cid,'Saved by Bob')['id'];self.s.keep(b,mid);self.now+=14*DAY
        self.assertEqual(self.s.messages(a,cid),[]);self.assertEqual(len(self.s.messages(b,cid)),1);self.s.unkeep(b,mid)
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
    def test_100_keepsakes_and_idempotent_saving(self):
        cid=self.conversation();a=self.a['user_id'];ids=[self.s.send(a,cid,str(i))['id'] for i in range(101)]
        for mid in ids[:100]:self.s.keep(a,mid)
        self.s.keep(a,ids[0]);self.assertEqual(len(self.s.keepsakes(a)),100);self.problem(409,self.s.keep,a,ids[100]);self.s.unkeep(a,ids[0]);self.s.keep(a,ids[100])
    def test_block_stops_discovery_and_messages(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];self.s.block(b,a);self.assertEqual(self.s.discover(a,'GU2',10),[]);self.problem(403,self.s.send,a,cid,'Blocked');self.problem(403,self.s.messages,a,cid)
    def test_reporting_still_works_after_blocking(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id']
        mid=self.s.send(a,cid,'Report this')['id'];self.s.block(b,a)
        self.assertIn('id',self.s.report(b,a,'Report after blocking',mid))
    def test_trial_expiry_and_calendar_month(self):
        self.now=self.a['trial_ends'];self.assertFalse(self.s.membership(self.a['user_id'])['active']);self.problem(402,self.s.discover,self.a['user_id'],'GU2')
        t=int(datetime(2028,1,31,10,tzinfo=timezone.utc).timestamp());self.assertEqual(datetime.fromtimestamp(advance_month(t),timezone.utc).day,29)
    def test_hidden_profiles_not_discovered(self):
        data=self.s.profile(self.b['user_id']);data['visible']=False;self.s.edit_profile(self.b['user_id'],data);self.assertEqual(self.s.discover(self.a['user_id'],'GU2',10),[])
    def test_account_deletion_cascades(self):
        cid=self.conversation();self.s.send(self.a['user_id'],cid,'Temporary');token,_=self.s.login('alice','A-long-test-passphrase');self.s.delete_account(self.a['user_id']);self.problem(401,self.s.authenticate,token);self.problem(404,self.s.messages,self.b['user_id'],cid)
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0)
    def test_report_evidence_has_separate_expiry(self):
        cid=self.conversation();a,b=self.a['user_id'],self.b['user_id'];mid=self.s.send(a,cid,'Reported evidence')['id'];self.s.report(b,a,'Test report',mid);self.now+=15*DAY;self.s.purge()
        with self.s.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM messages').fetchone()[0],0);self.assertEqual(self.s.dec(db.execute('SELECT evidence FROM reports').fetchone()[0]),'Reported evidence')
        self.now+=76*DAY;self.s.purge()
        with self.s.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM reports').fetchone()[0],0)
    def test_production_disabled(self):
        with self.assertRaises(RuntimeError):Service(Path(self.tmp.name)/'prod.sqlite3',Fernet.generate_key(),lambda:self.now,mode='production')
    def http(self,method,path,data=None,cookie='',csrf='',origin='http://127.0.0.1:8080',host='127.0.0.1:8080'):
        raw=json.dumps(data).encode() if data is not None else b'';out={};env=dict(REQUEST_METHOD=method,PATH_INFO=path,HTTP_HOST=host,HTTP_ORIGIN=origin,CONTENT_TYPE='application/json',CONTENT_LENGTH=str(len(raw)),REMOTE_ADDR='127.0.0.1',HTTP_COOKIE=cookie,HTTP_X_CSRF_TOKEN=csrf);env['wsgi.input']=io.BytesIO(raw)
        body=b''.join(self.app(env,lambda status,headers:out.update(status=int(status[:3]),headers=dict(headers))));return out,json.loads(body)
    def test_http_cookie_csrf_origin_and_no_payment_override(self):
        self.app=App(self.s);res,data=self.http('POST','/api/login',dict(login='alice',password='A-long-test-passphrase'));self.assertEqual(res['status'],200);cookie=res['headers']['Set-Cookie'].split(';')[0];self.assertIn('HttpOnly',res['headers']['Set-Cookie'])
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie);self.assertEqual(res['status'],403)
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie,csrf=data['csrf']);self.assertEqual(res['status'],200)
        res,_=self.http('POST','/api/discover',{'district':'GU2'},cookie=cookie,csrf=data['csrf'],origin='https://attacker.invalid');self.assertEqual(res['status'],403)
        res,_=self.http('GET','/api/health',host='attacker.invalid');self.assertEqual(res['status'],403)
        for path in ['/api/pay','/api/age-verified']:
            res,_=self.http('POST',path,{},cookie=cookie,csrf=data['csrf']);self.assertEqual(res['status'],404)
if __name__=='__main__':unittest.main()
