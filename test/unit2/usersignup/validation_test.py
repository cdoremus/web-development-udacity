'''
Created on Apr 25, 2012

@author: h87966
'''
import unittest
from unit2.usersignup.validation import UserSignupValidation
from unit2.usersignup.validation import VERIFICATION_MESSAGES
from unit2.usersignup.validation import VERIFICATION_MESSAGES_KEYS
from unit2.usersignup.validation import MISMATCHED_PASSWORDS_MESSAGE

class Test(unittest.TestCase):


    def setUp(self):
        self.validation = UserSignupValidation()
        pass


    def tearDown(self):
        pass



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

#    def testValid_BadVerifyPassword(self):
#        username = "Craig"
#        password = "c1"
#        verify = "c1"
#        email = "craig@foo.com"
#        validMsgs, isValid = self.validation.validate(username, password, verify, email)
#        self.assertFalse(isValid)
#        self.assertEquals(VERIFICATION_MESSAGES[VERIFICATION_MESSAGES_KEYS[2]], validMsgs[VERIFICATION_MESSAGES_KEYS[2]])
#        self.assertEmptyMessage([VERIFICATION_MESSAGES_KEYS[0],VERIFICATION_MESSAGES_KEYS[1],VERIFICATION_MESSAGES_KEYS[3]], validMsgs)

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

    def assertEmptyMessage(self, key_list, messages):
        for key in key_list:
            self.assertEquals('', messages[key], "Message with key " + key + " is not empty")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testValidateUsername']
    unittest.main()