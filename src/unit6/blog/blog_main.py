'''
Created on Apr 30, 2012

@author: h87966

Homework 3 - Basic blog

In order to be graded correctly for this homework, there are a 
few things to keep in mind. We'll be grading your web app by 
POSTing new blog entries to your form and checking that they 
appear on your blog's front page. There are a few main issues 
you need to keep in mind in order for this to work:
1. We assume your form to create new blog entries is at a path of 
'/newpost' from your blog's front page. That is, if your blog's 
front page is at 'www.myblog.com/blog', then the form is at 
'www.myblog.com/blog/newpost'.
2. The form method must be POST, not GET.
3. The form input boxes must have the names 'subject' and 'content' 
in order for the grading script to correctly post to them.
4. You must enter the full url into the supplied textbox above, 
including the path to your blog's front page. For example, 
our example app is running at http://cs253-homework-sean.appspot.com/blog, 
but if we instead only entered http://udacity-cs253.appspot.com/ then 
the grading script would not work.
5. Don't forget to escape your output!

My Notes from video:
1. Front page will list entries
2. A Form page to submit entries with a 'subject' and 'content' input
fields. Both fields are required and need to be validated with messages
3. Permalink page for each entry that has a unique url

Udacity basic blog app URL:
http://cs253-homework-sean.appspot.com/blog


My basic blog URL:
http://cdoremus-udacity-cs253.appspot.com/unit6


Unit 5 Instructions:
In order to be graded correctly for this homework, there are a few things to keep in mind. 
We'll be grading your web app by checking the JSON output on both the front page and permalink 
pages. Note that we still require all the functionality from previous homeworks.
We assume your frontpage JSON is at a location of "/.json from the URL you enter. That is, 
if you enter 'www.myblog.com/blog' in the text field above, then your frontpage JSON is 
at 'www.myblog.com/blog/.json'. We assume your permalink JSON is at ".json" from your 
permalink URLs.

See Video 14 on how to use json.dumps() to write json

HOMEWORK 6 Instructor Comments:

In order to be graded correctly for this homework, there are a few things to keep in mind. 
We'll be grading your web app by checking your front page for a string matching 
the regular expression:

QUERIED = re.compile("(?i)Queried\s+(\d+)\s+seconds?\s+ago")

And checking that it increments on subsequent requests. Note that we still require all the 
functionality from previous homeworks. We'll need to check timing values, so the grading 
script might take awhile to complete.

Submittal URL:
HW 6
http://cdoremus-udacity-cs253.appspot.com/unit6

'''
import time
import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from unit6.blog.blog_service import BlogService
from unit6.blog.blog_entry import BlogData
from unit6.blog.blog_datastore_factory import BlogDataStoreFactory


class BlogFrontPage(webapp2.RequestHandler):
    '''
    Front page controller for Homework 5 - Basic Blog
    '''


    def get(self):
        '''
        Handles initial get request
        '''
        self.response.headers['Content-Type'] = 'text/html'
        service = BlogService(BlogDataStoreFactory())
        blog_entries, last_queried = service.fetchAll()
        current = time.time()
        last_queried_all = current - last_queried
        values = {'blog_entries': blog_entries, "last_queried_all":last_queried_all}
        path = os.path.join(os.path.dirname(__file__), '../templates/blog.html')
        self.response.out.write(template.render(path, values))



class CreateBlogEntry(webapp2.RequestHandler):
    def get(self):
        '''
        Handles request for the create page
        '''
        self.response.headers['Content-Type'] = 'text/html'
        subject = self.request.get('subject')
        content = self.request.get('content')
        values = {'subject': subject, 'content':content}
        path = os.path.join(os.path.dirname(__file__), '../templates/create_blog_entry.html')
        self.response.out.write(template.render(path, values))
        
    def post(self):
        '''
        Handles blog entry creation
        '''
        self.response.headers['Content-Type'] = 'text/html'
        isValid = True
        values = {}
        subject = self.request.get('subject')
        if not subject:
            values['subject_error'] = 'Blog subject is required'
            isValid = False
        else:
            logging.info("Creating blog entry with subject: %s" % str(subject))
        content = self.request.get('content')
        if not content:
            values['content_error'] = 'Blog content is required'
            isValid = False
        else:
            logging.info("Creating blog entry with content: %s" % str(content))
        path = None
        if not isValid:
            values['subject'] = subject
            values['content'] = content
            path = os.path.join(os.path.dirname(__file__), '../templates/create_blog_entry.html')
            self.response.out.write(template.render(path, values))
        else:
            blog = BlogData(subject=subject, content=content) 
            service = BlogService(BlogDataStoreFactory())
            service.save(blog)
            blog_id = blog.key().id() 
            str_blog_id = str(blog_id)
            logging.info("Successfully posted blog entry. Redirectinr to '/unit6/%s" % str_blog_id  )  
            self.redirect('/unit6/%s' % str_blog_id)

class ShowBlogEntry(webapp2.RequestHandler):
    def get(self, entry_id):
        '''
        Handles displaying a blog entry
        '''
        self.response.headers['Content-Type'] = 'text/html'
#        entry_id = self.request.get('entry_id')
        service = BlogService(BlogDataStoreFactory())
        data = service.fetch(int(entry_id))
        last_queried_time = service.get_last_queried_time(entry_id)
        current = time.time()
        last_queried = current - last_queried_time     
        values = {'subject': data.subject, 'content':data.content, "last_queried": last_queried}
        path = os.path.join(os.path.dirname(__file__), '../templates/show_blog_entry.html')
        self.response.out.write(template.render(path, values))
        
class CreateBlogJson(webapp2.RequestHandler):

    def get(self, entry_id):
        '''
        Handles displaying a json for a blog entry
        '''
        self.response.headers['Content-Type'] = 'application/json'
        service = BlogService(BlogDataStoreFactory())
        blog_json = service.create_json(int(entry_id))
        self.response.out.write(blog_json)

class CreateBlogListJson(webapp2.RequestHandler):

    def get(self):
        '''
        Handles displaying a json for all blog entries
        '''
        self.response.headers['Content-Type'] = 'application/json'
        service = BlogService(BlogDataStoreFactory())
        blog_json = service.create_all_json()
        self.response.out.write(blog_json)

class FlushBlogCache(webapp2.RequestHandler):
    
    def get(self):
        '''
        Flushes the cache holding the blog and individual blog entries
        '''
        self.response.headers['Content-Type'] = 'text/html'
        service = BlogService(BlogDataStoreFactory())
        service.flush_blog_cache()
        logging.info("Blog flushed")  
        self.redirect('/unit6')