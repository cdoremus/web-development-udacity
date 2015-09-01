'''
Created on May 13, 2012

@author: h87966
'''
import unittest
from google.appengine.ext import testbed
from unit6.user.user_service import UserService
from unit6.user.user_datastore_factory import UserDataStoreFactory
from unit6.user.user_data import UserData
from unit6.user.user_error import LoginError, UserRegistrationError
from unit6.crypt import Crypt


class Test(unittest.TestCase):


    def setUp(self):
        # Setup mock GAE Data Store
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.service = UserService()
        factory = UserDataStoreFactory()
        self.storage = factory.get_storage()
        self.crypt = Crypt()


    def tearDown(self):
        self.testbed.deactivate()


    def testLogin(self):
        username = 'cdoremus'
        password = 'password'
        hashed_password = self.crypt.crypt_password(username, password)
        user = UserData(username=username, password=hashed_password)
        self.storage.save(user)
        user_id = user.key().id()
        cookie = self.crypt.make_cookie(user_id)
        new_cookie = self.service.login(username, password, cookie)
        self.assertFalse(new_cookie == None)
        self.assertEquals(user.key().id(), 1)

    def testLogin_Failed(self):
        username = 'cdoremus'
        password = 'password'
        hashed_password = self.crypt.crypt_password(username, password)
        user = UserData(username=username, password=hashed_password)
        self.storage.save(user)
        user_id = user.key().id()
        cookie = self.crypt.make_cookie(user_id)
        try: 
            self.service.login(username + 'foo', password, cookie)
            self.fail('Should not get here because LoginError should be raised due to bad usernames')
        except LoginError as error:
            self.assertEquals(error.validation_messages['login_error'], 'Invalid login')
            print error


    def testRegister(self):
        username = 'foobar'
        password = 'password'
        verify = password
        cookie = self.service.register(username=username, password=password, verify=verify)
        print cookie
        user = self.storage.fetchByUsername(username)
        self.assertFalse(cookie == None)
        user_id = user.key().id()
        self.assertEquals(user_id, 1)
        cookie_split = cookie.split('|')
        self.assertTrue(cookie_split[0] == str(user_id))
        self.assertFalse(cookie_split[1] == None)
        self.assertFalse(cookie_split[1] == '' )

    def testRegister_failed(self):
        username = 'foobar1'
        password = 'password'
        verify = password
        user = UserData(username=username, password=password)
        self.storage.save(user)
        try:
            self.service.register(username=username, password=password, verify=verify)
            self.fail('Should not get here because UserRegistrationError should be raised due to the fact that user already exists')
        except UserRegistrationError as error:
            self.assertEquals(error.validation_messages['user_exists_error'], 'That user already exists.')
            
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLogin']
    unittest.main()