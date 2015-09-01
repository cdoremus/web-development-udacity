'''
Created on May 22, 2012

@author: h87966
'''
import unittest
from unit6.blog.memcached_utils import MemcachedUtils
from google.appengine.ext import testbed


class Test(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.memcache = MemcachedUtils()

    def tearDown(self):
        self.testbed.deactivate()


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()