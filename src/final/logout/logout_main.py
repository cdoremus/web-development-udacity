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
from final.user.user_service import UserService
import logging

class LogoutUrl(webapp2.RequestHandler):
    '''
    Request Handler for logging out
    '''


    def get(self):
        '''
        Handles get requests
        '''
        self.response.headers['Content-Type'] = 'text/html'
        #delete user from data store
        user_id = self.request.cookies.get("user_id")
        if user_id:
            user_id = user_id[0:user_id.find('|')]
            service = UserService()
            logging.info("User %s logged out? %s" % (user_id, str(service.logout(user_id))))
        #clear cookie by setting it to an empty string
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/final/signup')
                