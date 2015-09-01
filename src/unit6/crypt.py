'''
Created on May 11, 2012

@author: h87966
'''
import random
import hashlib

class Crypt():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def crypt_user_id(self, user_id):
        secret = 'foobar forever!'
        hashed_user_id = hashlib.sha256(str(user_id) + secret).hexdigest()
        return hashed_user_id
    
    def is_valid_cookie(self, cookie):
        split_cookie = cookie.split('|')
        user_id = split_cookie[0]
        hashed_user_id = split_cookie[1]
        return hashed_user_id == self.crypt_user_id(user_id)
  
    def make_cookie(self, user_id):
        return '%s|%s' % (str(user_id), self.crypt_user_id(user_id))      
        
    def crypt_password(self, username, password, salt=None):
        if not salt:
            salt = self.salt()
        hashed_password = hashlib.sha256(username + password + salt).hexdigest()
        return '%s,%s' % (hashed_password, salt)

    def is_password_valid(self, username, password, hashed_val):
        salt = hashed_val.split(',')[1]
        return hashed_val == self.crypt_password(username, password, salt)
    
    
    def salt(self):
        salt = ''
        for i in range(0,5):
            rand = random.randint(48,122)
            salt += chr(rand)        
        return salt
    
    
    