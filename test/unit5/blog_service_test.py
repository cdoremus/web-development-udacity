'''
Created on May 17, 2012

@author: h87966
'''
import unittest
from google.appengine.ext import testbed
from unit5.blog_entry import BlogData
from unit5.blog_datastore_factory import BlogDataStoreFactory
from unit5.blog_service import BlogService


class Test(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.factory = BlogDataStoreFactory()
        self.storage = self.factory.get_storage()
        self.service = BlogService(self.factory)



    def tearDown(self):
        self.testbed.deactivate()


    def test_create_json(self):
        subject = 'Test Subject'
        content = 'Test Content'
        blog = BlogData(subject=subject,content=content)
        blog.put()
        blog_id = blog.key().id()
#        blog_data = self.service.fetch(blog_id)
        json_string = self.service.create_json(blog_id)
        self.assertTrue(('"subject": "%s"' % subject) in json_string, "Actual json string: " + str(json_string))
        self.assertTrue(('"content": "%s"' % content) in json_string, "Actual json string: " + str(json_string))

    def test_create_json_with_double_quotes(self):
        subject = 'Test"s Subject'
        content = 'Test"s Content'
        blog = BlogData(subject=subject,content=content)
        blog.put()
        blog_id = blog.key().id()
#        blog_data = self.service.fetch(blog_id)
        json_string = self.service.create_json(blog_id)
        self.assertTrue(('"subject": "%s"' % subject) in json_string, "Actual json string: " + str(json_string))
        self.assertTrue(('"content": "%s"' % content) in json_string, "Actual json string: " + str(json_string))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()