'''
Created on Apr 30, 2012

@author: h87966
'''
from unit5.json_utils import JsonUtils

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
    
    def create_json(self, blog_id):
        blog = self.fetch(blog_id)
        blog_json = JsonUtils.blog_to_json(blog)
        return blog_json

    def create_all_json(self):
        blog_list = self.fetchAll()
        return JsonUtils.blog_list_to_json(blog_list)
