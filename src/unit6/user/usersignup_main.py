'''
Created on Apr 25, 2012

@author: h87966



UNIT 2 HOMEWORK INSTRUCTIONS
Create a user signup page that validates a user's input
Fields
1. Username
2. Password
3. Verify Password
4. Email (optional)

Validation error message must show up next to the corresponding field

In order to be graded correctly for this homework, there are a few things 
to keep in mind. We'll be grading your web app by posting to your form and 
then checking the HTTP Response we receive. There are a few main issues you 
need to keep in mind in order for this to work:
The form elements where the user inputs their username, password, password again, 
and email address must be named "username", "password", "verify", and "email", 
respectively.
The form method must be POST, not GET.
Upon invalid user input, your web app should re-render the form for the user.
Upon valid user input, your web app should redirect to a welcome page for the user.
You must enter the full url into the supplied textbox above, including the path. 
For example, our example app is running at 
http://udacity-cs253.appspot.com/unit2/signup, but if we instead only 
entered http://udacity-cs253.appspot.com/ then the grading script would not work.

Regular Expressions
A regular expressions is a handy tool for matching text to a pattern. The regular expressions that we're using to validate you input are as follows:
Username: "^[a-zA-Z0-9_-]{3,20}$"
Password: "^.{3,20}$"
Email: "^[\S]+@[\S]+\.[\S]+$"
Example code for validating a username is as follows:
  import re
  USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
  def valid_username(username):
    return USER_RE.match(username)


UNIT 4 REGISTRATION HOMEWORK INSTRUCTIONS
Instructor Comments on the video page:
In order to be graded correctly for this homework, there are a few things to keep in mind. 
We'll be grading your web app by POSTing new users to your signup form and checking that we 
correctly get redirected and a cookie gets set. There are a few main issues you need to keep 
in mind in order for this to work:
1. We assume your form to signup new users is at a path of '/signup' from the url you enter. 
That is, if you enter 'www.myblog.com/blog' in the text field above, then the form is at 
'www.myblog.com/blog/signup'.
2. The form method must be POST, not GET.
3. The form input boxes must have the names 'username', 'password', 'verify', and 'email' in 
order for the grading script to correctly post to them.
4. Don't forget to escape your output!
Also, the basic methods you'll use to set and get cookies are as follows: In order to get a 
cookie you receive from the user, you can use 'self.request.cookies.get(name)', 
where name is the name of the cookie you are looking for. 
In order to send a cookie to a user, you simply add the header to your response. 
For example, 'self.response.headers.add_header('Set-Cookie', 'name=value; Path=/')', 
where name is the name of the cookie, and value is the value you're setting it to. The Path 
section of the header should be left as is for our purposes.
If you're interested in the css styling file we use for the example page, the link is here: 
http://udacity-cs253.appspot.com/static/main.css

Notes from the video:
Use signup for created in unit 2
Keep required and format validations from unit 2
Add validation for a person already registering with message
Have no user name in the welcome page URL, but show it on the page as: Welcome, <username>
The user must be registered (presumably in a Data Store table with the password hashed and salted.
A cookie needs to be set (named 'value' - see above). It needs to be pipe delimited with the value
and hash of the value. 
Use 'Edit This Cookie' Chrome Extension to test the cookie
An invaid cookie should redirect back to the signup page
If the user exists, then the user should be redirected to the signup page with the message: 
'That user already exists.'

Udacity Example URL:
http://udacity-cs253.appspot.com/signup
My URL:
http://cdoremus-udacity-cs253.appspot.com/blog/signup
    
'''
import webapp2
import os
from google.appengine.ext.webapp import template
from unit6.validation import UserSignupValidation
from unit6.user.user_service import UserService
from unit6.user.user_error import UserRegistrationError, InvalidCookieError
import logging

class UserSignupPage(webapp2.RequestHandler):
    '''
    Handles the user signup page
    '''


    def get(self):
        '''
        Handles initial get request
        '''
        self.response.headers['Content-Type'] = 'text/html'
        values = {'username':'', 'password':'','verify':'','email':''}
        validation = UserSignupValidation()
        validationMsgs = validation.initialize_messages_dict() 
        values.update(validationMsgs)
        path = os.path.join(os.path.dirname(__file__), '../templates/usersignup.html')
        self.response.out.write(template.render(path, values))
        
        
        
    def post(self):
        '''
        Handles post requests
        '''
        self.response.headers['Content-Type'] = 'text/html'
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        values = {'username':username, 'password':password,'verify':verify,'email':email}
        cookie = ''
        service = UserService()
        #Validate that user is not already registered
        isValid = False
        try:
            cookie = service.register(username=username, password=password, verify=verify, email=email)
            isValid = True
        except UserRegistrationError as error:
            path = os.path.join(os.path.dirname(__file__), '../templates/usersignup.html')
            values.update(error.validation_messages)
            self.response.out.write(template.render(path, values))
        if isValid:    
            self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % cookie)
            self.redirect('/unit6/welcome')
        
            
class UserSignupWelcome(webapp2.RequestHandler):
    '''
    Handles the user signup thanks page
    '''
    def get(self):
        '''
        Handles get request
        '''
#        values = {'username':self.request.get('username')}
        values = {}
        cookie = self.request.cookies.get('user_id')        
        service = UserService()
        user = None
        try:
            user = service.welcome(cookie)
            values['username'] = user.username
        except InvalidCookieError as error:
            logging.error('Invalid cookie in UserSignupWelcome: ' + str(error))
            self.redirect('/unit6/signup')
            
        path = os.path.join(os.path.dirname(__file__), '../templates/welcome.html')
        self.response.out.write(template.render(path, values))
        