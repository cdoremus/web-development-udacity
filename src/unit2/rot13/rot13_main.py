'''

In order to be graded correctly for this homework, there are a few things 
to keep in mind. We'll be grading your web app by POSTing to your form and 
retrieving the text that has been encoded with ROT13. There are a few main 
issues you need to keep in mind in order for this to work:

1. The textarea form element where the user inputs the text to encode must be 
named 'text'. In other words, you must have 'textarea name="text"' for us to post to.
2. The form method must be POST, not GET.
3. You must enter the full url into the supplied textbox above, including the 
path. For example, our example app is running at http://udacity-cs253.appspot.com/unit2/rot13, 
but if we instead only entered http://udacity-cs253.appspot.com/ then the grading script would not work.
4. Don't forget to escape your output!

VIDEO NOTES:
Rot13 increments every letter by 13
Getting to the end of the alphabet, the count of a letter backs upon itself.
For instance, z becomes m
Rot13 encrypting a string that has been Rot13 encrypted gets the original string.
Case must be preserved
Punctuation must be preserved
Also preserve whitespace
Escape the HTML

Udacity Test site
http://udacity-cs253.appspot.com/unit2/rot13

My Production URL:
http://cdoremus-udacity-cs253.appspot.com/unit2/rot13
'''
import os
import webapp2
from google.appengine.ext.webapp import template
from rot13 import Rot13

class Rot13MainPage(webapp2.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        values = {'rot13_string':''}
        path = os.path.join(os.path.dirname(__file__), 'rot13.html')
        self.response.out.write(template.render(path, values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        text = self.request.get('text')
        rot13 = Rot13()
        encrypted = rot13.encrypt(text) # escaping done in template using 'escape' attribute
        values = {'rot13_string':encrypted}
        path = os.path.join(os.path.dirname(__file__), 'rot13.html')
        self.response.out.write(template.render(path, values))
        