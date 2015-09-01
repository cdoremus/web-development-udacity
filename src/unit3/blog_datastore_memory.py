'''
Created on Apr 30, 2012

@author: h87966
'''
from unit3.blog_datastore import BlogDataStore

class BlogMemoryDataStore(BlogDataStore):
    '''
    Memory implementation of BlogDataStore
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.blog_entries = {}
        
    def save(self, blog_entry):
        entry_id = blog_entry.entry_id
        if not entry_id:
            entry_id = self.getMaxId() + 1
            
        self.blog_entries[entry_id] = blog_entry 
            
    
    def delete(self, entry_id):
        del self.blog_entries[entry_id] 
    
    def fetch(self, entry_id):
        return self.blog_entries.get(entry_id)
    
    def fetchAll(self):
        return self.blog_entries
    
    def getMaxId(self):
        max_id = 0
        for key in self.blog_entries.keys():
            if key > max_id:
                max_id = key
        return max_id