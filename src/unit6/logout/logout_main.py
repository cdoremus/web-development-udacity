'''
Created on May 9, 2012

@author: h87966

Instructor Comments:
Everything from usersignup_main.py - the following was added in bold to the bottom
regarding the Path attribute of Set-Cookie:
The default Path for a cookie is the current path, which is probably not what you want. 
The Path parameter should be / as in our example.    


Video Notes:
Logout url deletes the cookie and redirects to the signup page

'''
import webapp2

class LogoutUrl(webapp2.RequestHandler):
    '''
    classdocs
    '''


    def get(self):
        '''
        Constructor
        '''
        self.response.headers['Content-Type'] = 'text/html'
        #clear cookie by setting it to an empty string
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/unit6/signup')
                