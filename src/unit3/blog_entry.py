'''
Created on Apr 30, 2012

@author: h87966
'''
import datetime
from google.appengine.ext import db

class BlogData(db.Model):
    '''
    Data representation of a single blog entry
    '''
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    create_date = db.DateTimeProperty(auto_now_add=True)

