'''
Created on May 6, 2012

@author: h87966
'''
from google.appengine.ext import testbed
from google.appengine.api import memcache #@PydevCodeAnalysisIgnore (PyDev hack)
import unittest
from final.wiki.wiki_entry import WikiData
from final.wiki.wiki_datastore_appengine import WikiAppengineDataStore
from final.wiki.wiki_datastore_appengine import FETCH_ALL_CACHE_KEY,LAST_QUERY_CACHE_KEY_SUFFIX,DATA_CACHE_KEY_SUFFIX
import time
from datetime import datetime

class Test(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.storage = WikiAppengineDataStore()
        
    
    def tearDown(self):
        self.testbed.deactivate()

    def testPut(self):
        data = WikiData(url='Foo',content='Foo blog')
        data.put()
        pass

    def test_save_insert(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        b1a = self.storage.fetch(1)
        #assert not found
        self.assertTrue(b1a == None)
        self.storage.save(b1)
        b1a = self.storage.fetch(1)
        self.assertEquals(b1.url, b1a.url, "Wiki " + str(b1) + ' was not saved. This was saved instead: ' + str(b1a))
        self.assertEquals(b1.content, b1a.content, "Wiki " + str(b1) + ' was not saved. This was saved instead: ' + str(b1a))

    def test_save_update(self):
        b3 = WikiData(url='blog1',content='This is blog1')
        #insert
        self.storage.save(b3)
        b3a = self.storage.fetch(1)
        self.assertEquals(b3.url, b3a.url, "Wiki " + str(b3) + ' was not saved. This was saved instead: ' + str(b3a))
        self.assertEquals(b3.content, b3a.content, "Wiki " + str(b3) + ' was not saved. This was saved instead: ' + str(b3a))
        #update
        b3a.content='This is blog1 #2'
        self.storage.save(b3a)
        b3a2 = self.storage.fetch(1)
        self.assertEquals(b3.url, b3a2.url, "Wiki " + str(b3) + ' was not saved. This was saved instead: ' + str(b3a))
        self.assertNotEquals(b3.content, b3a2.content, "Wiki " + str(b3) + ' was not saved. This was saved instead: ' + str(b3a))

    def test_fetch(self):
        b = WikiData(url='blog1',content='This is blog1')
        expected = b.url 
        self.storage.save(b)
        b1 = self.storage.fetch(1)
        self.assertEquals(expected, b1.url, "Wiki with id " + str(expected) + ' was not found.')
        #check not found
        b1a = self.storage.fetch(100)
        self.assertTrue(b1a == None)
        pass

    def test_fetchAll(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b1)
        b2 = WikiData(url='blog2',content='This is blog2')
        self.storage.save(b2)
        expected = 2
        actual = list(self.storage.fetchAll())
        actual_count = len(actual)
        self.assertEquals(expected, actual_count, "Wiki count of " + str(expected) + ' size was not found. Actual count: ' + str(actual_count))
        print repr(actual)


    def test_fetchByUrl(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b1)
        b2 = WikiData(url='blog2',content='This is blog2')
        self.storage.save(b2)
        b3 = WikiData(url='blog1',content='This is blog2')
        self.storage.save(b3)
        actual = list(self.storage.fetchByUrl('blog1'))
        self.assertTrue(len(actual) == 2)

    def test_fetchAll_cacheTest(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b1)
        b2 = WikiData(url='blog2',content='This is blog2')
        self.storage.save(b2)
        b3 = WikiData(url='blog1',content='This is blog2')
        self.storage.save(b3)
        b4 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b4)
        b5 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b5)
        b6 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b6)
        
        actual_1 = list(self.storage.fetchAll())
        
        cache_key = FETCH_ALL_CACHE_KEY 
        actual_2 = memcache.get(cache_key)
        
        self.assertEquals(actual_1[0].content, actual_2[0].content)
        

    def test_fetch_cacheTest(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b1)
        b2 = WikiData(url='blog2',content='This is blog2')
        self.storage.save(b2)
        b3 = WikiData(url='blog1',content='This is blog2')
        self.storage.save(b3)
        b4 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b4)
        b5 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b5)
        b6 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b6)
        b5_id = b5.key().id()

        actual1 = self.storage.fetch(b5_id)
        
        cache_key = str(b5_id) + DATA_CACHE_KEY_SUFFIX 
        actual2 = memcache.get(cache_key)

        self.assertEquals(actual1.content, actual2.content)

    def test_fetchByUrl_cacheTest(self):
        b1 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b1)
        b2 = WikiData(url='blog2',content='This is blog2')
        self.storage.save(b2)
        b3 = WikiData(url='blog1',content='This is blog2')
        self.storage.save(b3)
        b4 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b4)
        b5 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b5)
        b6 = WikiData(url='blog1',content='This is blog1')
        self.storage.save(b6)

        actual1 = list(self.storage.fetchByUrl('blog1'))
        
        cache_key = 'blog1' + DATA_CACHE_KEY_SUFFIX 
        actual2 = memcache.get(cache_key)

        self.assertEquals(len(actual1), len(actual2))
        self.assertEquals(actual1[0].url, actual2[0].url)
        self.assertEquals(actual1[1].content, actual2[1].content)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPut']
    unittest.main()