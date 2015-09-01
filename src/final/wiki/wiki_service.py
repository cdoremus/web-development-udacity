'''
Created on Apr 30, 2012

@author: h87966
'''
from final.json_utils import JsonUtils
from wiki_datastore_appengine import FETCH_ALL_CACHE_KEY,LAST_QUERY_CACHE_KEY_SUFFIX,DATA_CACHE_KEY_SUFFIX
from google.appengine.api import memcache #@PydevCodeAnalysisIgnore (PyDev hack)

class WikiService():
    '''
    Service for obtaining and persisting blog data
    '''


    def __init__(self, wiki_datastore_factory):
        '''
        Constructor
        '''
        self.wiki_datastore = wiki_datastore_factory.get_storage()
        
    def fetchAll(self):
        return self.wiki_datastore.fetchAll()
    
    def save(self, wiki_entry):
        self.wiki_datastore.save(wiki_entry)
    
    def fetch(self, entry_id):
        return self.wiki_datastore.fetch(int(entry_id))
        
    def fetchCurrentUrl(self, url):
        wiki = self.wiki_datastore.fetchByUrl(url)
        if not wiki or len(wiki) == 0:
            return None
        else:
            return wiki[0]
        
    def fetchHistory(self, url):
        return self.wiki_datastore.fetchByUrl(url)

    def create_json(self, wiki_id):
        blog = self.fetch(wiki_id)
        wiki_json = JsonUtils.wiki_to_json(blog)
        return wiki_json
    
