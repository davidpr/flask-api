import unittest


from app import create_app#, db
class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client()
        # Creates a context for the appliation
        with self.app.app_context():
            print ('create context')
           
    def tearDown(self):
        with self.app.app_context():
            print ('delete context')
     