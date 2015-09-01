'''
Created on May 16, 2012

@author: h87966

JSON lecture notes
Json data structure: key-value pairs
1. Key - string
2. Value - one of the data types

Json Data types
1. list
2. int
3. float
4. boolean
5. string

null == [] (empty list

'''
from datetime import datetime
import unittest
from unit5.json_utils import JsonUtils
from unit5.blog_entry import BlogData
from google.appengine.ext import testbed
from unit5.blog_datastore_appengine import BlogAppengineDataStore



class Test(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.storage = BlogAppengineDataStore()


    def tearDown(self):
        pass


    def test_BlogToJson(self):
        blog = BlogData(subject="Test1", content="Test1 blog content")
        self.storage.save(blog)
        blog_id = blog.key().id()
        stored_blog = self.storage.fetch(blog_id)
        actual = JsonUtils.blog_to_json(stored_blog);
        self.assertTrue('"subject": "Test1"' in actual,"Blog subject not parsed correctly in blog data: " + repr(actual))
        self.assertTrue('"content": "Test1 blog content"' in actual,"Blog content not parsed correctly in blog data: " + repr(actual))
        
    def test_BlogToJson_with_single_quote(self):
        blog = BlogData(subject="Test1", content="Test1 blog's content")
        self.storage.save(blog)
        blog_id = blog.key().id()
        stored_blog = self.storage.fetch(blog_id)
        actual = JsonUtils.blog_to_json(stored_blog);
        self.assertTrue('"subject": "Test1"' in actual,"Blog subject not parsed correctly in blog data: " + repr(actual))
        self.assertTrue('"content": "Test1 blog\'s content"' in actual,"Blog content not parsed correctly in blog data: " + repr(actual))

    def test_BlogToJson_with_double_quote(self):
        blog = BlogData(subject="Test1", content='Test1 blog"s content')
        self.storage.save(blog)
        blog_id = blog.key().id()
        stored_blog = self.storage.fetch(blog_id)
        actual = JsonUtils.blog_to_json(stored_blog);
        self.assertTrue('"subject": "Test1"' in actual,"Blog subject not parsed correctly in blog data: " + repr(actual))
        self.assertTrue('"content": "Test1 blog\\"s content"' in actual,"Blog content not parsed correctly in blog data: " + repr(actual))

    def test_BlogListToJson(self):
        blog1 = BlogData(subject="Test1", content='Test1 blog content')
        self.storage.save(blog1)
        blog2 = BlogData(subject="Test2", content='Test2 blog content')
        self.storage.save(blog2)
        blog_list = self.storage.fetchAll()
        actual = JsonUtils.blog_list_to_json(blog_list);
        print actual
        print str(len(actual))
        self.assertFalse(len(actual) == 0)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreate']
    unittest.main()