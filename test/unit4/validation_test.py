'''
Created on Apr 25, 2012

@author: h87966
'''
import unittest
from unit4.user_data import UserData
from unit4.validation import UserSignupValidation, LoginValidation
from unit4.validation import VERIFICATION_MESSAGES
from unit4.validation import VERIFICATION_MESSAGES_KEYS
from unit4.validation import MISMATCHED_PASSWORDS_MESSAGE
from google.appengine.ext import testbed
from unit4.user_datastore_appengine import UserAppengineDataStore
from unit4.crypt import Crypt

class Test(unittest.TestCase):


    def setUp(self):
        # Setup mock GAE Data Store
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        #instantiate classes under test
        self.validation = UserSignupValidation()
        self.validation_login = LoginValidation()
        self.user_datastore = UserAppengineDataStore()
        self.crypt = Crypt()


    def tearDown(self):
        self.testbed.deactivate()

    def testIsValidUsername(self):
        self.assertTrue(self.validation.is_valid_username("Crag"))
        self.assertTrue(self.validation.is_valid_username("Crag-Doremus"))
        self.assertTrue(self.validation.is_valid_username("Crag_Doremus"))
        self.assertTrue(self.validation.is_valid_username("Cra"))
        self.assertFalse(self.validation.is_valid_username("ca"))
        self.assertFalse(self.validation.is_valid_username("cat!"))
        self.assertTrue(self.validation.is_valid_username("abcdefghijklmnopqrst"))
        self.assertFalse(self.validation.is_valid_username("abcdefghijklmnopqrstu"))
        pass

    def testIsValidPassword(self):
        self.assertTrue(self.validation.is_valid_password("Craig"))
        self.assertTrue(self.validation.is_valid_password("abcdefghijklmnopqrst"))
        self.assertFalse(self.validation.is_valid_password("abcdefghijklmnopqrstu"))
        pass

    def testIsValidEmail(self):
        self.assertTrue(self.validation.is_valid_email("Craig@foo.com"))
        self.assertTrue(self.validation.is_valid_email("Craig@foo.com.com"))
        self.assertFalse(self.validation.is_valid_email("Craigfoocom"))
        pass

    def testValid(self):
        username = "Craig"
        password = "craig1"
        verify = "craig1"
        email = "craig@foo.com"
#        user = UserData(username=username, password=password, email=email)
#        self.user_datastore.save(user)
        validMsgs, isValid = self.validation.validate(username, password, verify, email)
        self.assertTrue(isValid)
        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[0],VERIFICATION_MESSAGES_KEYS[1],VERIFICATION_MESSAGES_KEYS[2],VERIFICATION_MESSAGES_KEYS[3]], validMsgs)
        
    def testValid_BadUsername(self):
        username = "Craigasdfasdfasdfasdfadfadfs"
        password = "craig1"
        verify = "craig1"
        email = "craig@foo.com"
        validMsgs, isValid = self.validation.validate(username, password, verify, email)
        self.assertFalse(isValid)
        self.assertEquals(VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[0]], validMsgs[VERIFICATION_MESSAGES_KEYS[0]])
        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[1],VERIFICATION_MESSAGES_KEYS[2],VERIFICATION_MESSAGES_KEYS[3]], validMsgs)
        
    def testUserExists_True(self):
        username = 'cdoremus'
        #add a record to the data store
        userData = UserData(username=username, password='password')
        self.user_datastore.save(userData)
        self.assertTrue(self.validation.user_exists(username), "User " + username + " does not exist")


    def testUserExists_False(self):
        username = 'cdoremus1'
        testVal ='foo'
        #add a record to the data store
        userData = UserData(username=username, password='password')
        self.user_datastore.save(userData)
        self.assertFalse(self.validation.user_exists(testVal), "User " + testVal + " exists. User added: " + userData.username)

    def testValidate_UserExists(self):
        '''
        Test validate() with a user that already exists
        '''
        username = 'cdoremus'
        password = 'password'
        
        #add a record to the data store
        userData = UserData(username=username, password=password)
        self.user_datastore.save(userData)
        #verify in database
        user = self.user_datastore.fetchByUsername(username)
        print user.username
        self.assertTrue(self.validation.validate(username=username, password=password, verify=password, email=None), "User " + username + " exists")

    def testValid_BadPassword(self):
        username = "Craig"
        password = "c1"
        verify = "c1"
        email = "craig@foo.com"
        validMsgs, isValid = self.validation.validate(username, password, verify, email)
        self.assertFalse(isValid)
        self.assertEquals(VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[1]], validMsgs[VERIFICATION_MESSAGES_KEYS[1]])
        self.assertEquals(VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[2]], validMsgs[VERIFICATION_MESSAGES_KEYS[2]])
        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[0],VERIFICATION_MESSAGES_KEYS[3]], validMsgs)

    def testValid_BadEmail(self):
        username = "Craig"
        password = "craig1"
        verify = "craig1"
        email = "craigfoo.com"
        validMsgs, isValid = self.validation.validate(username, password, verify, email)
        self.assertFalse(isValid)
        self.assertEquals(VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[3]], validMsgs[VERIFICATION_MESSAGES_KEYS[3]])
        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[0],VERIFICATION_MESSAGES_KEYS[2],VERIFICATION_MESSAGES_KEYS[1]], validMsgs)

    def testValid_PasswordsDontMatch(self):
        username = "Craig"
        password = "craig1"
        verify = "craig"
        email = "craig@foo.com"
        validMsgs, isValid = self.validation.validate(username, password, verify, email)
        self.assertFalse(isValid)
        self.assertEquals(MISMATCHED_PASSWORDS_MESSAGE, validMsgs[VERIFICATION_MESSAGES_KEYS[1]])
        self.assertEquals(MISMATCHED_PASSWORDS_MESSAGE, validMsgs[VERIFICATION_MESSAGES_KEYS[2]])
        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[0],VERIFICATION_MESSAGES_KEYS[3]], validMsgs)

    def test_is_password_and_verify_equals(self):
        self.assertTrue(self.validation.is_password_and_verify_equals("craig", "craig"))
        self.assertFalse(self.validation.is_password_and_verify_equals("craig", "craig1"))

    def test_validate_login(self):
        username = 'foo'
        password = 'bar'
        hashed_password = self.crypt.crypt_password(username, password)
        user = UserData(username=username, password=hashed_password)
        self.user_datastore.save(user)
        
        msgs, isValid = self.validation_login.validate(username, password)
        self.assertTrue(isValid)
        self.assertTrue(len(msgs) == 0)

    def test_validate_login_username_notfound(self):
        username = 'foo'
        password = 'bar'
        user = UserData(username=username,password=password)
        self.user_datastore.save(user)
        
        msgs, isValid = self.validation_login.validate(username + 'foo', password)
        self.assertFalse(isValid)
        self.assertFalse(len(msgs) == 0)

    def test_validate_login_invalid_password(self):
        username = 'foo'
        password = 'bar'
        hashed_password = self.crypt.crypt_password(username, password)
        user = UserData(username=username, password=hashed_password)
        self.user_datastore.save(user)
        
        msgs, isValid = self.validation_login.validate(username, password + 'bar')
        self.assertFalse(isValid)
        self.assertFalse(len(msgs) == 0)
        
    def assertEmptyMessage(self, key_list, messages):
        for key in key_list:
            self.assertEquals('', messages[key], "Message with key " + key + " is not empty")

            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testValidateUsername']
    unittest.main()