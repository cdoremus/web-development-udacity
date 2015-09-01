'''
Created on Apr 25, 2012

@author: h87966
'''

import os
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from unit1.hello_udacity import HelloUdacityMainPage
from unit2.rot13.rot13_main import Rot13MainPage
from unit2.usersignup.usersignup_main import UserSignupMainPage, UserSignupRedirect
#from unit3.blog_main import BlogFrontPage, CreateBlogEntryPage, SaveBlogEntry,\
#from unit4.registration.usersignup_main import UserSignupPage, UserSignupWelcome
#from unit4.login.login_main import LoginPage
#from unit4.logout.logout_main import LogoutUrl
#import unit5.registration
#import unit6.registration
#import unit6.login
#import unit5.login
#import unit6.logout
#import unit5.logout
#from unit6.user.usersignup_main import UserSignupPage, UserSignupWelcome
#from unit6.login.login_main import LoginPage
#from unit6.logout.logout_main import LogoutUrl
#from unit6.blog.blog_main import BlogFrontPage, CreateBlogEntry, ShowBlogEntry,\
#    CreateBlogJson, CreateBlogListJson, FlushBlogCache
#from unit5.registration.usersignup_main import UserSignupPage, UserSignupWelcome
#from unit5.login.login_main import LoginPage
#from unit5.logout.logout_main import LogoutUrl
#from unit5.blog_main import BlogFrontPage, ShowBlogEntry, CreateBlogJson, CreateBlogListJson, CreateBlogEntry

from final.user.usersignup_main import UserSignupPage, UserSignupWelcome
from final.login.login_main import LoginPage
from final.logout.logout_main import LogoutUrl
from final.wiki.wiki_main import ShowWikiEntry, ShowWikiHistory, EditWikiEntry

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

class MainPage(webapp2.RequestHandler):
            
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        values = {'title_string':''}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, values))
    
application = webapp2.WSGIApplication([
                                       ('/', MainPage),
                                       ('/unit1/hello', HelloUdacityMainPage),
                                       ('/unit2/rot13', Rot13MainPage),
                                       ('/unit2/usersignup', UserSignupMainPage),
                                       ('/unit2/usersignup/thanks', UserSignupRedirect),
#                                       ('/unit3/blog', BlogFrontPage),
#                                       ('/unit3/blog/newpost', CreateBlogEntryPage),
#                                       ('/unit3/save_blog_entry', SaveBlogEntry),
#                                       ('/unit3/show_blog_entry', ShowBlogEntry),
#                                       ('/unit4/blog/signup', UserSignupPage),
#                                       ('/unit4/blog/welcome', UserSignupWelcome),
#                                       ('/unit4/blog/login', LoginPage),
#                                       ('/unit4/blog/logout', LogoutUrl),

#                                       ('/unit5/signup', unit5.registration.usersignup_main.UserSignupPage),
#                                       ('/unit5/welcome', unit5.registration.usersignup_main.UserSignupWelcome),
#                                       ('/unit5/login', unit5.login.login_main.LoginPage),
#                                       ('/unit5/logout', unit5.logout.logout_main.LogoutUrl),
#                                       ('/unit5', unit5.blog_main.BlogFrontPage),
#                                       ('/unit5/newpost', unit5.blog_main.CreateBlogEntry),
#                                       ('/unit5/([0-9]+)', unit5.blog_main.ShowBlogEntry),
#                                       ('/unit5/([0-9]+).json', unit5.blog_main.CreateBlogJson),
#                                       ('/unit5/.json', unit5.blog_main.CreateBlogListJson),

#                                       ('/unit6/signup', UserSignupPage),
#                                       ('/unit6/welcome', UserSignupWelcome),
#                                       ('/unit6/login', LoginPage),
#                                       ('/unit6/logout', LogoutUrl),
#                                       ('/unit6', BlogFrontPage),
#                                       ('/unit6/newpost', CreateBlogEntry),
#                                       ('/unit6/([0-9]+)', ShowBlogEntry),
#                                       ('/unit6/([0-9]+).json', CreateBlogJson),
#                                       ('/unit6/.json', CreateBlogListJson),
#                                       ('/unit6/flush', FlushBlogCache)

                                       ('/final/signup', UserSignupPage),
                                       ('/final/welcome', UserSignupWelcome),
                                       ('/final/login', LoginPage),
                                       ('/final/logout', LogoutUrl),
                                       ('/final/_edit' + PAGE_RE, EditWikiEntry),
                                       ('/final/_history' + PAGE_RE, ShowWikiHistory),
#                                       ('final' + PAGE_RE, ShowWikiEntry)                                       
                                       (PAGE_RE, ShowWikiEntry)                                       
                                       ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
