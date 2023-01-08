from . import BaseTestClass

class ServerTestCase(BaseTestClass):
    def test_root(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'OK', res.data)

    def test_test(self):
        res = self.client.get('/test')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Test OK', res.data)


   