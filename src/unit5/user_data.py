'''
Created on May 10, 2012

@author: h87966
'''
from google.appengine.ext import db

class UserData(db.Model):
    '''
    User data persisted to GAE Data Store
    '''
    
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    create_date = db.DateTimeProperty(auto_now_add=True)
    mod_date = db.DateTimeProperty(auto_now=True)