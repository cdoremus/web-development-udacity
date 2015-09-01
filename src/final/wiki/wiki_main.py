'''
Created on Apr 30, 2012

@author: h87966

Submittal URL for final:
http://cdoremus-udacity-cs253.appspot.com/final

'''
import time
import webapp2
import os
import logging
from google.appengine.ext.webapp import template
from final.wiki.wiki_service import WikiService
from final.wiki.wiki_entry import WikiData
from final.wiki.wiki_datastore_factory import WikiDataStoreFactory
from final.webapp_utils import WebappUtils
from final.user.user_error import InvalidCookieError
from final.user.user_service import UserService

class WikiFrontPage(webapp2.RequestHandler):
    '''
    Front page controller for Final - Basic Wiki
    '''


    def get(self):
        '''
        Handles initial get request
        '''
        self.response.headers['Content-Type'] = 'text/html'
        check_cookie(self)
        service = WikiService(WikiDataStoreFactory())
        wiki_entries, last_queried = service.fetchAll()
        current = time.time()
        last_queried_all = current - last_queried
        values = {'wiki_entries': wiki_entries, "last_queried_all":last_queried_all}
        path = os.path.join(os.path.dirname(__file__), '../templates/wiki.html')
        self.response.out.write(template.render(path, values))



class EditWikiEntry(webapp2.RequestHandler):
    def get(self, foo=None):
        '''
        Handles request for the create page
        '''
        logging.info("Running EditWikiEntry.get()")
        self.response.headers['Content-Type'] = 'text/html'
        check_cookie(self)
        wiki_id = self.request.get('wiki_id')
        data = None
        service = WikiService(WikiDataStoreFactory())
        url = ''
        if wiki_id:
            data = service.fetch(wiki_id)
        else:
            url = WebappUtils.getLastPathElement(self.request)
            data = service.fetchCurrentUrl(url)
        logging.info('Data: %s' % (str(data)))
        values = {'url': url, 'content':''}
        if data:
            values = {'url': data.url, 'content': data.content}
        path = os.path.join(os.path.dirname(__file__), '../templates/edit_wiki_entry.html')
        self.response.out.write(template.render(path, values))
        
    def post(self, param=None):
        '''
        Handles wiki entry creation
        '''
        logging.info("Running EditWikiEntry.post()")
        logging.info('Parameter=%s' % param)
        self.response.headers['Content-Type'] = 'text/html'
        check_cookie(self)
        isValid = True
        values = {}
#        url = self.request.get('url')
        url = WebappUtils.getLastPathElement(self.request);
        if not url:
            url = param[1:]
        if not url:
            values['url_error'] = 'Wiki url is required'
            isValid = False
        else:
            logging.info("Creating wiki entry with url: %s" % str(url))
        content = self.request.get('content')
        if not content:
            values['content_error'] = 'Wiki content is required'
            isValid = False
        else:
            logging.info("Creating wiki entry with content: %s" % str(content))
        path = None
        if not isValid:
            values['url'] = url
            values['content'] = content
            path = os.path.join(os.path.dirname(__file__), '../templates/edit_wiki_entry.html')
            self.response.out.write(template.render(path, values))
        else:
            wiki = WikiData(url=url, content=content) 
            service = WikiService(WikiDataStoreFactory())
            logging.info("Saving WikiData: %s" % str_WikiData(wiki))
            service.save(wiki)
            logging.info("Successfully posted wiki entry. Redirecting to '/final/%s" % url  )  
            self.redirect('/final/%s' % url)

class ShowWikiEntry(webapp2.RequestHandler):
    def get(self, entry_id):
        '''
        Handles displaying a wiki entry
        '''
        logging.info("Running ShowWikiEntry.get()")        
        logging.info("Request path: %s" % str(self.request.path))
        self.response.headers['Content-Type'] = 'text/html'
        check_cookie(self)
        wiki_id = self.request.get('wiki_id')
        data = None
        service = WikiService(WikiDataStoreFactory())
        if wiki_id:
            data = service.fetch(int(wiki_id))
        else:
            url = WebappUtils.getLastPathElement(self.request)
            if not url:
                url = 'WikiFrontPage'
            logging.info('url: %s' % str(url))
            data = service.fetchCurrentUrl(url)
        if data:
            logging.info('Getting WikiData: %s' % str_WikiData(data))
        else:
            logging.info('No data found')            
        values = {'wiki': data}
        if not data:
            redirect = '/final/_edit/%s' % url
            logging.info("Data not found for wiki. Redirecting to edit page: %s" % redirect)
            self.redirect(redirect)
        else:
            path = os.path.join(os.path.dirname(__file__), '../templates/show_wiki_entry.html')
            self.response.out.write(template.render(path, values))

class ShowWikiHistory(webapp2.RequestHandler):
    def get(self, entry_id):
        '''
        For showing wiki history
        '''
        logging.info("Running ShowWikiHistory.get()")        
        self.response.headers['Content-Type'] = 'text/html'
        check_cookie(self)
        url = WebappUtils.getLastPathElement(self.request)
        service = WikiService(WikiDataStoreFactory())
        data = service.fetchHistory(url)
        values = {'wiki_entries':data, "url": url}
        path = os.path.join(os.path.dirname(__file__), '../templates/history.html')
        self.response.out.write(template.render(path, values))
        
        
def check_cookie(request_handler):
    try:
        cookie = request_handler.request.cookies.get("user_id")
        user_service = UserService()
        user_service.check_cookie(cookie)
    except InvalidCookieError as error:
        request_handler.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        request_handler.redirect('/final/signup')

def str_WikiData(wiki):
    string = ''
    if wiki:
        string = 'WikiData[url=%s ; content=%s]' % (wiki.url, wiki.content)
    return string
