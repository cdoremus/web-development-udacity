'''
Created on Apr 24, 2012


@author: h87966


'''

class Rot13(object):
    '''
    Does Rot13 encryption
    '''
    A_num = ord('A')
    Z_num = ord('Z')
    a_num = ord('a')
    z_num = ord('z')

    def __init__(self):
        '''
        Constructor
        '''
    
    def encrypt(self, string):
        '''
        Encrypts a string using rot13
        '''
        encrypted = ''
        for char in string:
            enc_char = char
            num_char = ord(char)
#            print "char:" + char + " num_char: " + str(num_char)
            if num_char in range(self.A_num, self.Z_num + 1):
                enc_char = self.rot13(char, self.A_num, self.Z_num)
            elif num_char in range(self.a_num, self.z_num + 1):
                enc_char = self.rot13(char, self.a_num, self.z_num)
#            print "enc_char: " + enc_char
            encrypted = encrypted + enc_char
        return encrypted 
    
    def rot13(self, char, start, end):
        '''
        Does Rot13 on a single character
        '''
        rot13_char = None
        if not char:
            return char
        ord_char = ord(char)
        if ord_char in range(start, end + 1):
            num = ord_char + 13
            if num > end: #we've gone past the end
                diff = num - end
                rot13_char = chr(start + diff - 1)
            else:
                rot13_char = chr(num)
        else:
            rot13_char = char
        return rot13_char
                