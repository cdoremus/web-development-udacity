'''
Created on Apr 25, 2012

@author: h87966
'''
import re
from google.appengine.ext import db
from unit5.user_datastore_factory import UserDataStoreFactory
from unit5.crypt import Crypt

VERIFICATION_MESSAGES_KEYS = ['username_error','password_error','verify_error',
                              'email_error', 'user_exists_error', 'login_error']
                            

VERIFICATION_MESSAGES = {
                         VERIFICATION_MESSAGES_KEYS[0]:'The username format is not valid',
                         VERIFICATION_MESSAGES_KEYS[1]:'The password format is not valid',
                         VERIFICATION_MESSAGES_KEYS[2]:'The verification password format is not valid',
                         VERIFICATION_MESSAGES_KEYS[3]:'The email format is not valid',
                         VERIFICATION_MESSAGES_KEYS[4]:'That user already exists.',
                         VERIFICATION_MESSAGES_KEYS[5]:'Invalid login'
                         }

MISMATCHED_PASSWORDS_MESSAGE = 'The Password and Verify Password fields do not match'

#VALIDATION_MESSAGES = {
#                          VERIFICATION_MESSAGES_KEYS[0]:'',
#                          VERIFICATION_MESSAGES_KEYS[1]:'',
#                          VERIFICATION_MESSAGES_KEYS[2]:'',
#                          VERIFICATION_MESSAGES_KEYS[3]:''
#                          }

class UserSignupValidation():
    '''
    Validates username, password and email fields from the user signup form
    '''


    def __init__(self):
        '''
        Constructor
        '''
#        self.initialize_messages_dict()
        factory = UserDataStoreFactory()
        self.user_datastore = factory.get_storage()
        
        pass

    def validate(self, username, password, verify, email):
        is_valid = True
        passwords_match = True
        validation_messages = self.initialize_messages_dict( )
        #verify matching passwords
        if not self.is_password_and_verify_equals(password, verify):
            validation_messages[VERIFICATION_MESSAGES_KEYS[1]] =  MISMATCHED_PASSWORDS_MESSAGE
            validation_messages[VERIFICATION_MESSAGES_KEYS[2]] = MISMATCHED_PASSWORDS_MESSAGE
            passwords_match = False
            is_valid = False
        #validate username
        if not self.is_valid_username(username):
            validation_messages[VERIFICATION_MESSAGES_KEYS[0]] = VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[0]]
            is_valid = False
        #validate password
        if not self.is_valid_password(password) and passwords_match:
            validation_messages[VERIFICATION_MESSAGES_KEYS[1]] =  VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[1]]
            is_valid = False
        #validate verify
        if not self.is_valid_password(verify) and passwords_match:
            validation_messages[VERIFICATION_MESSAGES_KEYS[2]] = VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[2]]
            is_valid = False
        #validate email
        if not self.is_valid_email(email):
            validation_messages[VERIFICATION_MESSAGES_KEYS[3]] = VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[3]]
            is_valid = False
        #validate that user does not already exist
        if self.user_exists(username):
            validation_messages[VERIFICATION_MESSAGES_KEYS[4]] = VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[4]]
            is_valid = False    
        return validation_messages, is_valid

    def initialize_messages_dict(self):
        messages = {
                          VERIFICATION_MESSAGES_KEYS[0]:'',
                          VERIFICATION_MESSAGES_KEYS[1]:'',
                          VERIFICATION_MESSAGES_KEYS[2]:'',
                          VERIFICATION_MESSAGES_KEYS[3]:''
                          }
        return messages;

    def is_password_and_verify_equals(self, password, verify):
        return password == verify

    def is_valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)
        
    def is_valid_password(self, password):
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        return PASSWORD_RE.match(password)

    def is_valid_email(self, email):
        if not email:
            return True
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        return EMAIL_RE.match(email)
   
    def user_exists(self, username):
        user_exists = False
        user = self.user_datastore.fetchByUsername(username)
#        print 'user found in user_exists(): ' + str(user)
        if user:
            user_exists = True
            
        return user_exists
                   


class LoginValidation():
    
    def __init__(self):
        factory = UserDataStoreFactory()
        self.user_datastore = factory.get_storage()
        self.crypt = Crypt()
        pass
                
    def validate(self, username, password):
        validation_messages = {} 
        is_valid = False
        if not self.is_valid_login(username, password):
            is_valid = False
            validation_messages[VERIFICATION_MESSAGES_KEYS[5]] = VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[5]]           
        else:
            is_valid = True
        return validation_messages, is_valid 
   
    def is_valid_login(self, username, password):
        is_valid = False
        user = self.user_datastore.fetchByUsername(username)
        if user:
            user_pwd_hashed = user.password
            if self.crypt.is_password_valid(username, password, user_pwd_hashed):
                is_valid = True
        return is_valid 

