'''
Created on May 11, 2012

@author: h87966
'''
import unittest
from unit6.crypt import Crypt


class Test(unittest.TestCase):


    def setUp(self):
        self.crypt = Crypt()
        pass


    def tearDown(self):
        pass


    def testSalt(self):
        done = []
        for i in range(1,100):
            salt = self.crypt.salt()
            self.assertFalse(salt in done)
            done.append(salt)
        pass

    def testCryptPassword(self):
        username = 'craig'
        password = 'craig1'
        hashed_val = self.crypt.crypt_password(username, password)
        isValid = self.crypt.is_password_valid(username, password, hashed_val)
        self.assertTrue(isValid)

    def testCryptPassword_Fails(self):
        username = 'craig'
        password = 'craig1'
        hashed_val = self.crypt.crypt_password(username, password)
        isValid = self.crypt.is_password_valid(username + 'foo', password, hashed_val)
        self.assertFalse(isValid)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()