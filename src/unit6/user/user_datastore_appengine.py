'''
Created on Apr 30, 2012

@author: h87966
'''
from google.appengine.ext import db
from unit6.user.user_datastore import UserDataStore
from    .user_data import UserData

class UserAppengineDataStore(UserDataStore):
    '''
    AppEngine implementation of UserDataStore
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def save(self, user):
            
        user.put()
        #get back id
        new_user = self.fetchByUsername(user.username)
        new_user.user_id = user.key().id()
        return new_user 
            
    
    def delete(self, entry_id):
        pass
    
    def fetch(self, user_id):
        user = UserData.get_by_id(user_id)
        user.user_id = user.key().id()

        return user
    
    def fetchAll(self):
        sql = "select * from UserData order by create_date"
        user_entries = db.GqlQuery(sql)
        for user in user_entries:
            user.user_id = user.key().id()
        return user_entries

    def fetchByUsername(self, username):
        sql = "select * from UserData where username='%s'" % username 
        userfound = None
        user_entries = db.GqlQuery(sql)
        for user in user_entries:
            user.user_id = user.key().id()
            userfound = user
            break #after first record
        return userfound
    