'''
Created on May 11, 2012

@author: h87966
'''
import unittest
from google.appengine.ext import testbed
from unit4.user_data import UserData
from unit4.user_datastore_appengine import UserAppengineDataStore


class Test(unittest.TestCase):
    

    def setUp(self):
        # Setup mock GAE Data Store
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.user_datastore = UserAppengineDataStore()

    def tearDown(self):
        self.testbed.deactivate()


    def testFetch(self):
        user = UserData(username='cdoremus', password='password')
        user.put()
        user_id = user.key().id()
        actual = self.user_datastore.fetch(user_id)
        self.assertEquals(user.username, actual.username, "Found user: " + str(actual.username))
        self.assertTrue(actual.user_id == 1, "Found user_id: " + str(actual.user_id))

    def testSave(self):
        user = UserData(username='cdoremus', password='password')
        new_user = self.user_datastore.save(user)
        user_id = user.key().id()
        actual = self.user_datastore.fetch(user_id)
        self.assertEquals(user.username, actual.username, "Found user: " + str(actual.username))
        self.assertTrue(new_user.user_id ==1, 'New user_id: ' + str(new_user.user_id))
    
    def testFetchAll(self): 
        user1 = UserData(username='cdoremus1', password='password')
        new_user1 = self.user_datastore.save(user1)
        user2 = UserData(username='cdoremus2', password='password')
        new_user2 = self.user_datastore.save(user2)
        users = self.user_datastore.fetchAll()
        self.assertTrue(users.count() == 2, "User count: " + str(users.count()))
        self.assertTrue(new_user1.user_id ==1, 'New user_id for user1: ' + str(new_user1.user_id))
        self.assertTrue(new_user2.user_id ==2, 'New user_id for user2: ' + str(new_user2.user_id))
#        count = 0
#         for user in users:
#            count += 1
#            self.assertTrue(user.user_id == count)
           
    def testFetchByUsername(self): 
        user1 = UserData(username='cdoremus1', password='password1')
        self.user_datastore.save(user1)
        user2 = UserData(username='cdoremus2', password='password2')
        self.user_datastore.save(user2)
        userfound1 = self.user_datastore.fetchByUsername('cdoremus1')
        self.assertEquals(userfound1.password, user1.password, 'Found user' + str(userfound1))
        self.assertTrue(userfound1.user_id == 1,"User id is not 1: " + str(userfound1.user_id))

    def testFetchByUsername_NotFound(self): 
        user1 = UserData(username='cdoremus1', password='password1')
        self.user_datastore.save(user1)
        user2 = UserData(username='cdoremus2', password='password2')
        self.user_datastore.save(user2)
        userfound1 = self.user_datastore.fetchByUsername('foo')
        self.assertTrue(userfound1 == None, 'Found user' + str(userfound1))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFetch']
    unittest.main()