'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db
from unit3.blog_datastore import BlogDataStore
from unit3.blog_entry import BlogData

class BlogAppengineDataStore(BlogDataStore):
    '''
    AppEngine implementation of BlogDataStore
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def save(self, blog_entry):
#        entry_id = blog_entry.entry_id
#        if not entry_id:
#            blog_entry.entry_id = self.getMaxId() + 1
            
        blog_entry.put() 
            
    
    def delete(self, entry_id):
        pass
    
    def fetch(self, entry_id):
#        blog_entry = None
#        sql = "select * from BlogData where entry_id=" + entry_id
        blog_entry = BlogData.get_by_id(entry_id)
#        blog_entries = db.GqlQuery(sql)
#        for entry in blog_entries:
#            blog_entry = entry

        return blog_entry
    
    def fetchAll(self):
        sql = "select * from BlogData order by create_date"
        blog_entries = db.GqlQuery(sql)
        for entry in blog_entries:
            entry.entry_id = entry.key().id()
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