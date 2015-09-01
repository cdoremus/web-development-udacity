'''
Created on May 16, 2012

@author: h87966
'''
import json
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

class JsonUtils():
    
    @staticmethod
    def blog_to_json(blog_entry):
        return json.dumps(JsonUtils.blog_to_strdict(blog_entry))
    
    @staticmethod
    def blog_to_strdict(blog_entry):
        subject = blog_entry.subject
        content = blog_entry.content
        created = blog_entry.created
        str_created = created.strftime(DATETIME_FORMAT)
        last_modified = blog_entry.last_modified 
        str_last_modified = last_modified.strftime(DATETIME_FORMAT)
        data = {"subject":subject, "content":content, "created":str_created, "last_modified":str_last_modified}        
        return data 
        
    
    @staticmethod
    def blog_list_to_json(blog_list):
        dict_list = []
        for blog in blog_list:
            dict_list.append(JsonUtils.blog_to_strdict(blog))
        return json.dumps(dict_list)
