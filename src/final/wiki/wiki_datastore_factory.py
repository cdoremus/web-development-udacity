'''
Created on Apr 30, 2012

@author: h87966
'''
from final.wiki.wiki_datastore_appengine import WikiAppengineDataStore

class WikiDataStoreFactory():
    '''
    classdocs
    '''
    storage_implementations = {'appengine':WikiAppengineDataStore()}

    def __init__(self, storage_impl='appengine'):
        '''
        Constructor
        '''
        self.storage = self.storage_implementations[storage_impl]
    
    def set_storage(self, wiki_storage):
        self.storage = wiki_storage
            
    def get_storage(self):
        return self.storage
    