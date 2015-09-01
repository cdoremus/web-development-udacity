'''
Created on May 11, 2012

@author: h87966
'''
class UserRegistrationError():
    
    def __init__(self, validation_messages):
        self.validation_messages = validation_messages 
    
    def __str__(self):
        return repr(self.validation_messages)        
    
    
class LoginError():
    
    def __init__(self, validation_messages):
        self.validation_messages = validation_messages 

    def __str__(self):
        return repr(self.validation_messages)        
    
class InvalidCookieError():
    
    def __init__(self):
        pass

