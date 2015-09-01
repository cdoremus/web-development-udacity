'''
Created on May 29, 2012

@author: h87966
'''
import unittest
from final.webapp_utils import WebappUtils
from google.appengine.ext.webapp.mock_webapp import MockRequest, MockResponse
import logging
import re


class Test(unittest.TestCase):

    def setUp(self):
        self.request = MockRequest()
        pass


    def tearDown(self):
        pass


    def test_getLastPathElement(self):
        self.request.set_path('/final/wiki')
#        print "Test path: %s " % str(self.request.get_path())
        self.assertEquals('wiki', WebappUtils.getLastPathElement(self.request))

    def test_getLastPathElement_withQueryString(self):
        self.request.set_path('/final/wiki?user_id=foo&url=bar')
#        print "Test path: %s " % str(self.request.get_path())
        self.assertEquals('wiki', WebappUtils.getLastPathElement(self.request))

    def test_getLastPathElement_context_path_only(self):
        self.request.set_path('/final')
#        print "Test path: %s " % str(self.request.get_path())
        self.assertTrue(WebappUtils.getLastPathElement(self.request) == None)
        
    def test_mockResponse(self):
        response = MockResponse()
#        response.out = 'foo'
        response.out.write('<html>')
        print response.out.getvalue()
        
    def test_regex(self):
        PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
        path = "/foo"
        self.assertTrue(re.match(PAGE_RE, path))    
        path = "/"
        self.assertTrue(re.match(PAGE_RE, path))    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_getLastPathElement']
    unittest.main()