'''
Created on Apr 30, 2012

@author: h87966
'''

class BlogService():
    '''
    classdocs
    '''


    def __init__(self, blog_datastore_factory):
        '''
        Constructor
        '''
        self.blog_datastore = blog_datastore_factory.get_storage()
        
    def fetchAll(self):
        return self.blog_datastore.fetchAll()
        pass
    
    def save(self, blog_entry):
        self.blog_datastore.save(blog_entry)
        pass
    
    def fetch(self, entry_id):
        return self.blog_datastore.fetch(entry_id)
        pass
        