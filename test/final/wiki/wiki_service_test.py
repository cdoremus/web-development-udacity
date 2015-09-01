'''
Created on May 17, 2012

@author: h87966
'''
import unittest
from google.appengine.ext import testbed
from final.wiki.wiki_entry import WikiData
from final.wiki.wiki_datastore_factory import WikiDataStoreFactory
from final.wiki.wiki_service import WikiService


class Test(unittest.TestCase):


    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.factory = WikiDataStoreFactory()
        self.storage = self.factory.get_storage()
        self.service = WikiService(self.factory)



    def tearDown(self):
        self.testbed.deactivate()


    def test_create_json(self):
        url = 'Test Subject'
        content = 'Test Content'
        wiki = WikiData(url=url,content=content)
        wiki.put()
        wiki_id = wiki.key().id()
#        wiki_data = self.service.fetch(wiki_id)
        json_string = self.service.create_json(wiki_id)
        self.assertTrue(('"url": "%s"' % url) in json_string, "Actual json string: " + str(json_string))
        self.assertTrue(('"content": "%s"' % content) in json_string, "Actual json string: " + str(json_string))

    def test_create_json_with_double_quotes(self):
        url = 'Test"s Subject'
        content = 'Test"s Content'
        wiki = WikiData(url=url,content=content)
        wiki.put()
        wiki_id = wiki.key().id()
#        wiki_data = self.service.fetch(wiki_id)
        json_string = self.service.create_json(wiki_id)
        quote = url.find('"')
        json_url = url[0:quote] + '\\' + url[quote:]
        quote = content.find('"')
        json_content = content[0:quote] + '\\' + content[quote:]
        self.assertTrue(('"url": "%s"' % json_url) in json_string, "Actual json string: " + str(json_string))
        self.assertTrue(('"content": "%s"' % json_content) in json_string, "Actual json string: " + str(json_string))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()