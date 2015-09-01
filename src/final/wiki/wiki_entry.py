'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db

class WikiData(db.Model):
    '''
    Data representation of a single wiki entry
    '''
    url = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    
    def __str__(self):
        string = 'WikiData{subject=%s' % WikiData.url
        string += '; content=%s' % WikiData.content
        string += '; created=%s' % str(WikiData.created)
        string += '}'
        return string

