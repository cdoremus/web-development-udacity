'''
Created on May 11, 2012

@author: h87966
'''
from final.user.user_datastore_factory import UserDataStoreFactory
from final.user.user_data import UserData
from final.user.user_error import UserRegistrationError, LoginError,\
    InvalidCookieError
from final.validation import UserSignupValidation, LoginValidation
from final.crypt import Crypt

class UserService(object):
    '''
    User service
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.storage = UserDataStoreFactory().get_storage()
        self.signup_validation = UserSignupValidation();
        self.login_validation = LoginValidation();
        self.crypt = Crypt()
        
    def register(self, username,password,verify, email=None):
        validation_msgs, isValid = self.signup_validation.validate(username=username, password=password, verify=verify, email=email)
        if not isValid:
            raise UserRegistrationError(validation_msgs)
        else:
            crypt_password = self._crypt_password(username, password)
            user = UserData(username=username,password=crypt_password,email=email)
            saved_user = self.storage.save(user)
            user_id = saved_user.key().id()
        return self.crypt.make_cookie(user_id)
    
    def login(self,username,password, cookie):
        self.check_cookie(cookie)
        validation_msgs, login_ok = self.login_validation.validate(username, password)
        if not login_ok:
            raise LoginError(validation_msgs)
        user = self.storage.fetchByUsername(username)
        user_id = user.user_id
        return self.crypt.make_cookie(user_id)

    def logout(self, user_id):
        user = self.storage.fetch(int(user_id))
        user.delete()

    def welcome(self, cookie):
        self.check_cookie(cookie)
        user_id = cookie.split('|')[0]
        user = self.storage.fetch(int(user_id))
        return user
    
    def check_cookie(self, cookie):
        if not cookie:
            raise InvalidCookieError()
        else: 
            cookie_ok = self.crypt.is_valid_cookie(cookie)
            if not cookie_ok:
                raise InvalidCookieError()

    def get_user(self, user_id):
        return self.storage.fetch(int(user_id))
    
    def _crypt_password(self, username, password):
        return self.crypt.crypt_password(username, password)
    
    def _hash_user_id(self, user_id):
        return self.crypt.crypt_user_id(user_id)
        