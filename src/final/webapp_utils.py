'''
Created on May 29, 2012

@author: h87966
'''
import logging


CONTEXT_PATH = '/final'

class WebappUtils(object):
    '''
    classdocs
    '''

    @staticmethod
    def getLastPathElement(request):
        '''
        Gets the final path element rom the request url, excluding the querystring
        returns None if the slash cannot be found or if it is the first character in the path
        '''
        path = str(request.path)
        last_slash = path.rfind('/')
        if last_slash == 0 or last_slash == -1:
            return None
        last_questionmark = path.rfind('?')
        last_path_element = None
        if last_questionmark != -1:
            last_path_element = path[last_slash + 1: last_questionmark]       
        else:
            last_path_element = path[last_slash + 1:]        
        return last_path_element