'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db

class BlogData(db.Model):
    '''
    Data representation of a single blog entry
    '''
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    last_queried = None
    
    def __str__(self):
        string = 'BlogData{subject=%s' % BlogData.subject
        string += '; content=%s' % BlogData.content
        string += '; created=%s' % str(BlogData.created)
        string += '}'
        return string

