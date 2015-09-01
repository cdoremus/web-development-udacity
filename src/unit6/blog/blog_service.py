'''
Created on Apr 30, 2012

@author: h87966
'''
from unit6.json_utils import JsonUtils
from blog_datastore_appengine import FETCH_ALL_CACHE_KEY,LAST_QUERY_CACHE_KEY_SUFFIX,DATA_CACHE_KEY_SUFFIX
from google.appengine.api import memcache #@PydevCodeAnalysisIgnore (PyDev hack)

class BlogService():
    '''
    Service for obtaining and persisting blog data
    '''


    def __init__(self, blog_datastore_factory):
        '''
        Constructor
        '''
        self.blog_datastore = blog_datastore_factory.get_storage()
        
    def fetchAll(self):
        return self.blog_datastore.fetchAll(), self.blog_datastore.getLastQueried(FETCH_ALL_CACHE_KEY + LAST_QUERY_CACHE_KEY_SUFFIX)
    
    def save(self, blog_entry):
        self.blog_datastore.save(blog_entry)
        pass
    
    def fetch(self, entry_id):
        return self.blog_datastore.fetch(entry_id)
        pass
    
    def create_json(self, blog_id):
        blog = self.fetch(blog_id)
        blog_json = JsonUtils.blog_to_json(blog)
        return blog_json

    def create_all_json(self):
        blog_list = self.fetchAll()
        return JsonUtils.blog_list_to_json(blog_list)
    
    def get_last_queried_time(self, key):
        return self.blog_datastore.getLastQueried(str(key) + LAST_QUERY_CACHE_KEY_SUFFIX)
    
    def flush_blog_cache(self):
        #purge FETCH_ALL_CACHE_KEY cached value
        memcache.set(FETCH_ALL_CACHE_KEY, None)
        #purge individual entries        
        blog_entries = self.blog_datastore.fetchAll()
        for blog_entry in blog_entries:
            entry_id = blog_entry.key().id()
            cache_key = str(entry_id) + DATA_CACHE_KEY_SUFFIX
            memcache.set(cache_key, None)
    
