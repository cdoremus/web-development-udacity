'''
Created on Apr 30, 2012

@author: h87966
'''

from final.user.user_datastore_appengine import UserAppengineDataStore

class UserDataStoreFactory():
    '''
    Factory for getting a UserDataStore implementation
    '''
    storage_implementations = {'appengine':UserAppengineDataStore()}
    
    def __init__(self, storage_impl='appengine'):
        '''
        Constructor
        '''
        self.storage = self.storage_implementations[storage_impl]
    
    def set_storage(self, user_storage):
        self.storage = user_storage
            
    def get_storage(self):
        return self.storage
    