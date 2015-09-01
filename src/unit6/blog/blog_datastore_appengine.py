'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db
#from google.appengine.api import memcache

from unit6.blog.blog_datastore import BlogDataStore
from unit6.blog.blog_entry import BlogData
import time
from google.appengine.api import memcache #@PydevCodeAnalysisIgnore (PyDev hack)
import math

FETCH_ALL_CACHE_KEY = "FETCH_ALL"
DATA_CACHE_KEY_SUFFIX = "_DATA" #blog_id will be the prefix
LAST_QUERY_CACHE_KEY_SUFFIX = "_LAST_MOD"

class BlogAppengineDataStore(BlogDataStore):
    '''
    AppEngine implementation of BlogDataStore
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def save(self, blog_entry):
        blog_entry.put()
        #purge  FETCH_ALL_CACHE_KEY cached value
        memcache.set(FETCH_ALL_CACHE_KEY, None)
        #purge cache keyed to current blog_id
        blog_id = blog_entry.key().id()         
        last_queried_key = str(blog_id) + LAST_QUERY_CACHE_KEY_SUFFIX 
        memcache.set(last_queried_key, None)
        
            
    
    def delete(self, entry_id):
        pass
    
    def fetch(self, entry_id):
        cache_key = str(entry_id) + DATA_CACHE_KEY_SUFFIX
        last_queried_key = str(entry_id) + LAST_QUERY_CACHE_KEY_SUFFIX 
        blog_entry = memcache.get(cache_key)
        if not blog_entry:
            blog_entry = BlogData.get_by_id(entry_id)
            memcache.set(cache_key, blog_entry)
            self.setLastQueried(last_queried_key)
        return blog_entry
    
    def fetchAll(self):
        blog_entries = memcache.get(FETCH_ALL_CACHE_KEY)
        last_queried_key = FETCH_ALL_CACHE_KEY + LAST_QUERY_CACHE_KEY_SUFFIX 
        if not blog_entries:
#            print "Query run"
            sql = "select * from BlogData order by created"
            blog_entries = list(db.GqlQuery(sql))
            memcache.set(FETCH_ALL_CACHE_KEY, blog_entries)
            self.setLastQueried(last_queried_key)
            for entry in blog_entries:
                entry.entry_id = entry.key().id()
#        else:
#            print "Found in cache"
        return blog_entries
    
    def getMaxId(self):
        max_id = 0
        blog_entries = self.fetchAll()
        for entry in blog_entries:
            entry_id = entry.entry_id
            if max_id >= entry_id:
                max_id = entry_id
        if not max_id:
            max_id = 0
        return max_id
    
    def setLastQueried(self, key):
        cache_key = str(key)
        current = time.time()
        memcache.set(cache_key, current)

    def getLastQueried(self, key):
        cache_key = str(key)
        return memcache.get(cache_key)
