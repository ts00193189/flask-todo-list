from unittest import TestCase
from todo import create_app, db


class BasicTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.client = None
