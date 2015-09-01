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
http://cdoremus-udacity-cs253/unit3/blog

'''
import webapp2
import os
from google.appengine.ext.webapp import template
from unit3.blog_service import BlogService
from unit3.blog_entry import BlogData
from unit3.blog_datastore_factory import BlogDataStoreFactory


class BlogFrontPage(webapp2.RequestHandler):
    '''
    Front page controller for Homework 3 - Basic Blog
    '''


    def get(self):
        '''
        Handles initial get request
        '''
        self.response.headers['Content-Type'] = 'text/html'
        service = BlogService(BlogDataStoreFactory())
        blog_entries = service.fetchAll()
        values = {'blog_entries': blog_entries}
        path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, values))



class CreateBlogEntryPage(webapp2.RequestHandler):
    def get(self):
        '''
        Handles request for the create page
        '''
        self.response.headers['Content-Type'] = 'text/html'
        subject = self.request.get('subject')
        content = self.request.get('content')
        values = {'subject': subject, 'content':content}
        path = os.path.join(os.path.dirname(__file__), 'create_blog_entry.html')
        self.response.out.write(template.render(path, values))
        

class SaveBlogEntry(webapp2.RequestHandler):
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
        content = self.request.get('content')
        if not content:
            values['content_error'] = 'Blog content is required'
            isValid = False
        path = None
        if not isValid:
            values['subject'] = subject
            values['content'] = content
            path = os.path.join(os.path.dirname(__file__), 'create_blog_entry.html')
        else:
            blog = BlogData(subject=subject, content=content) 
            service = BlogService(BlogDataStoreFactory())
            service.save(blog)        
            blog_entries = service.fetchAll()
            values['blog_entries'] = blog_entries
            path = os.path.join(os.path.dirname(__file__), 'blog.html')
        self.response.out.write(template.render(path, values))

class ShowBlogEntry(webapp2.RequestHandler):
    def get(self):
        '''
        Handles displaying a blog entry
        '''
        self.response.headers['Content-Type'] = 'text/html'
        entry_id = self.request.get('entry_id')
        service = BlogService(BlogDataStoreFactory())
        data = service.fetch(int(entry_id))
        values = {'subject': data.subject, 'content':data.content}
        path = os.path.join(os.path.dirname(__file__), 'show_blog_entry.html')
        self.response.out.write(template.render(path, values))
        
