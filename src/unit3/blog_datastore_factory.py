'''
Created on Apr 30, 2012

@author: h87966
'''
from unit3.blog_datastore_memory import BlogMemoryDataStore
from unit3.blog_datastore_appengine import BlogAppengineDataStore

class BlogDataStoreFactory():
    '''
    classdocs
    '''
    storage_implementations = {'memory':BlogMemoryDataStore(),
                               'appengine':BlogAppengineDataStore()}

    def __init__(self, storage_impl='appengine'):
        '''
        Constructor
        '''
        self.storage = self.storage_implementations[storage_impl]
    
    def set_storage(self, blog_storage):
        self.storage = blog_storage
            
    def get_storage(self):
        return self.storage
    