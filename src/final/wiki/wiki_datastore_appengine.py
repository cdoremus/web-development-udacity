'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db
#from google.appengine.api import memcache

from final.wiki.wiki_datastore import WikiDataStore
from final.wiki.wiki_entry import WikiData
import time
from google.appengine.api import memcache #@PydevCodeAnalysisIgnore (PyDev hack)
import math

FETCH_ALL_CACHE_KEY = "FETCH_ALL"
DATA_CACHE_KEY_SUFFIX = "_DATA" #wiki_id will be the prefix
LAST_QUERY_CACHE_KEY_SUFFIX = "_LAST_MOD"

class WikiAppengineDataStore(WikiDataStore):
    '''
    AppEngine implementation of WikiDataStore
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def save(self, wiki_entry):
        '''
        Saves data  in GAE data store and resets cache for fetchAll(),
        fetch() and fetchBuUrl() 
        '''
        wiki_entry.put()
        #resets cached fetchAll() data memcached by FETCH_ALL_CACHE_KEY cached value
        memcache.set(FETCH_ALL_CACHE_KEY, None)
        wiki_id = wiki_entry.key().id()         
        #resets cached fetch() memcached entries keyed to current wiki_id
        last_queried_key = str(wiki_id) + LAST_QUERY_CACHE_KEY_SUFFIX 
        memcache.set(last_queried_key, None)
        last_queried_key = str(wiki_id) + DATA_CACHE_KEY_SUFFIX 
        memcache.set(last_queried_key, None)
        #resets cached fetchByUrl() memcached entries keyed to url
        last_queried_key = str(wiki_entry.url) + LAST_QUERY_CACHE_KEY_SUFFIX 
        memcache.set(last_queried_key, None)
        last_queried_key = str(wiki_entry.url) + DATA_CACHE_KEY_SUFFIX 
        memcache.set(last_queried_key, None)
            
    
    def delete(self, entry_id):
        pass
    
    def fetch(self, entry_id):
        cache_key = str(entry_id) + DATA_CACHE_KEY_SUFFIX
        last_queried_key = str(entry_id) + LAST_QUERY_CACHE_KEY_SUFFIX 
        wiki_entry = memcache.get(cache_key)
        if not wiki_entry:
            wiki_entry = WikiData.get_by_id(entry_id)
            memcache.set(cache_key, wiki_entry)
            self.setLastQueried(last_queried_key)
        return wiki_entry
    
    def fetchAll(self):
        wiki_entries = memcache.get(FETCH_ALL_CACHE_KEY)
        last_queried_key = FETCH_ALL_CACHE_KEY + LAST_QUERY_CACHE_KEY_SUFFIX 
        if not wiki_entries:
#            print "Query run"
            sql = "select * from WikiData order by created desc"
            wiki_entries = list(db.GqlQuery(sql))
            memcache.set(FETCH_ALL_CACHE_KEY, wiki_entries)
            self.setLastQueried(last_queried_key)
            for entry in wiki_entries:
                entry.entry_id = entry.key().id()
#        else:
#            print "Found in cache"
        return wiki_entries
 
    
    def fetchByUrl(self, url):
        cache_key = str(url) + DATA_CACHE_KEY_SUFFIX
        last_queried_key = str(url) + LAST_QUERY_CACHE_KEY_SUFFIX 
        wiki_entries = memcache.get(cache_key)
        if not wiki_entries:
            sql = "select * from WikiData where url='%s' order by created desc" % url
            wiki_entries = list(db.GqlQuery(sql))
            for entry in wiki_entries:
                entry.entry_id = entry.key().id()
            memcache.set(cache_key, wiki_entries)
            self.setLastQueried(last_queried_key)
        return wiki_entries
    
    def getMaxId(self):
        max_id = 0
        wiki_entries = self.fetchAll()
        for entry in wiki_entries:
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
