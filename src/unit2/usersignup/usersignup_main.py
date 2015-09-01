'''
Created on Apr 25, 2012

@author: h87966

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

URL:
http://cdoremus-udacity-cs253.appspot.com/unit2/usersignup
    
'''
import webapp2
import os
from google.appengine.ext.webapp import template
import cgi
from unit2.usersignup.validation import UserSignupValidation

class UserSignupMainPage(webapp2.RequestHandler):
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
        path = os.path.join(os.path.dirname(__file__), 'usersignup.html')
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
        validation = UserSignupValidation()
        validationMsgs, isValid = validation.validate(username, password, verify, email)
#        values = self.escape_values(values) 
        values.update(validationMsgs)
        path = os.path.join(os.path.dirname(__file__), 'usersignup.html')
        if isValid:
            self.redirect('/unit2/usersignup/thanks?username=' + username)
        else:
            self.response.out.write(template.render(path, values))

    def escape_values(self, values):
        new_values = {}
        for value in values:
            new_values[value] = cgi.escape(values[value])
        return new_values
        
            
class UserSignupRedirect(webapp2.RequestHandler):
    '''
    Handles the user signup thanks page
    '''
    def get(self):
        '''
        Handles get request
        '''
        values = {'username':self.request.get('username')}
        path = os.path.join(os.path.dirname(__file__), 'welcome.html')
        self.response.out.write(template.render(path, values))
        