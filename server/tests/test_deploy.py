from turtle import rt
from . import BaseTestClass

class ServerTestCase(BaseTestClass):
    # test a normal petition
    def test_deploy1(self):
        with self.app.app_context():

            res = self.client.post('/deploy', data=dict( \
                r="512" , \
                w="script.py", \
                rt="python3.8", \
                c="2", \
                p="agnostic"
            ))
            self.assertEqual(200, res.status_code)
            self.assertIn(b'<!DOCTYPE html>\n<html lang="en">\n<p>CLI petition was: am deploy -r 512 -w script.py -rt python3.8 -c 2 -p agnostic. Petition UUID:', res.data)
            
    # test a petition that will contain generate the default values 
    def test_deploy2(self):
        with self.app.app_context():

            res = self.client.post('/deploy', data=dict( \
                r="512" , \
                w="script.py", \
                rt="python3.8"
            ))
            self.assertEqual(200, res.status_code)
            self.assertIn(b'<!DOCTYPE html>\n<html lang="en">\n<p>CLI petition was: am deploy -r 512 -w script.py -rt python3.8 -c 1 -p agnostic. Petition UUID:', res.data)