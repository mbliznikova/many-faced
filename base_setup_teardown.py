import unittest
from selenium import webdriver
import os


class BaseTestCase(unittest.TestCase):
    app_address = os.environ['APP_ADDRESS']
    hub_address = os.environ['HUB_ADDRESS']
    desired_capabilities = {
        'platform': os.environ['TEST_PLATFORM'],
        'browserName': os.environ['TEST_BROWSER'],
    }

    @classmethod
    def setUpClass(cls):
        if cls is not BaseTestCase and cls.setUp is not BaseTestCase.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseTestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride


    def setUp(self):
        self.driver = webdriver.Remote(self.hub_address,
                                       self.desired_capabilities)
        self.driver.get(self.app_address)

    def tearDown(self):
        self.driver.quit()
