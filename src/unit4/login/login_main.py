'''
Created on May 9, 2012

@author: h87966

See Instructor Comment notes in usersignup_main.py


Video Notes:
Page contains two fields (from signup):
1. Username: 
2. Password:
If username does not exist or password does not match, then an error message
is displayed on the login page: 'Invalid login"
Entering a valid username and password redirects the user to the welcome page
Welcome page has the same cookie as when doing the registration (signup) use case:
- the cookie gets set on a successful login


Udacity Example URL:
http://udacity-cs253.appspot.com/login


'''
import logging
import os
import webapp2
from google.appengine.ext.webapp import template
from unit4.validation import LoginValidation
from unit4.user_service import UserService
from unit4.user_error import LoginError, InvalidCookieError

class LoginPage(webapp2.RequestHandler):
    '''
    classdocs
    '''
    
    def get(self):
        '''
        Shows login page
        '''
        self.response.headers['Content-Type'] = 'text/html'
        
        path = os.path.join(os.path.dirname(__file__), 'login.html')
        self.response.out.write(template.render(path, {}))

    def post(self):
        '''
        Processes user login
        '''
        self.response.headers['Content-Type'] = 'text/html'
        username = self.request.get('username')
        password = self.request.get('password')
        values = {'username': username, 'password': password}
        cookie = self.request.cookies.get('user_id')
        service = UserService()
        new_cookie = ''
        isError = False
        try:
            new_cookie = service.login(username=username,password=password, cookie=cookie)
        except InvalidCookieError as error:
            isError = True
            self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
            self.redirect('/unit4/blog/signup')
        except LoginError as error:
            isError = True
            messages = error.validation_messages
            logging.info("LoginErrlr msgs:" + str(messages))
            values.update(messages)
            path = os.path.join(os.path.dirname(__file__), 'login.html')
            self.response.out.write(template.render(path, values))
        if not isError:
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % new_cookie)
#            self.redirect('/unit4/blog/welcome?username=%s' % username)
            self.redirect('/unit4/blog/welcome')
            