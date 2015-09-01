'''
Created on Apr 24, 2012

@author: h87966
'''
import unittest
import urllib
from unit2.rot13.rot13 import Rot13

class Test(unittest.TestCase):
    lower_start = ord('a')
    lower_end = ord('z')
    upper_start = ord('A')
    upper_end = ord('Z')

    def setUp(self):
        self.rot13 = Rot13()
        
        pass


    def tearDown(self):
        pass


    def test_encrypt(self):
        string = 'AZaz]-/'
        expected = 'NMnm]-/'
        actual = self.rot13.encrypt(string)
        self.assertEquals(expected, actual, 'encrypt() did not work. Actual: ' + actual)

    def test_encrypt_hello(self):
        string = 'Hello'
        expected = 'Uryyb'
        actual = self.rot13.encrypt(string)
        self.assertEquals(expected, actual, 'encrypt() did not work. Actual: ' + actual)

    def test_encrypt_round_trip(self):
        string = 'Craig1234!@#$-/'
        expected = string
        encrypted = self.rot13.encrypt(string)
        #re-encrypt back to original
        actual = self.rot13.encrypt(encrypted)
        self.assertEquals(expected, actual, 'encrypt() did not work. Actual: ' + actual)
        
    def test_encrypt_hello_multiple_words(self):
        string = 'Hello  Hello  Hello'
        expected = 'Uryyb  Uryyb  Uryyb'
        actual = self.rot13.encrypt(string)
        self.assertEquals(expected, actual, 'encrypt() did not work. Actual: ' + actual)

    def test_encrypt_hello_multiple_lines(self):
        string = 'Hello\nHello\nHello'
        expected = 'Uryyb\nUryyb\nUryyb'
        actual = self.rot13.encrypt(string)
        self.assertEquals(expected, actual, 'encrypt() did not work. Actual: ' + actual)

    def test_rot13_uppercase(self):
        char = 'A'
        expected = 'N'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'rot13() does not work. Actual: ' + actual)
        char = 'H'
        expected = 'U'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'rot13() does not work. Actual: ' + actual)
        char = '.'
        expected = '.'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'rot13() does not work: ' + actual)
        char = 'Z'
        expected = 'M'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'rot13() does not work: ' + actual)
        char = 'O'
        expected = 'B'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
 
    def test_rot13_lowercase(self):
        char = 'a'
        expected = 'n'
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = 'h'
        expected = 'u'
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = ' '
        expected = ' '
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = 'z'
        expected = 'm'
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = 'o'
        expected = 'b'
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
                  
    def test_rot13_non_alphas(self):
        char = ' '
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '@'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '#'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '$'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '~'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = ''
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)

    def test_rot13_non_printables(self):
        char = '\n'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '\t'
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        #same checks with uppercase start and end
        char = '\n'
        expected = '\n'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        self.assertEquals(expected, actual, 'Actual does not work: ' + actual)
        char = '\t'
        expected = '\t'
        actual = self.rot13.rot13(char, self.upper_start, self.upper_end)
        #Test None
        char = None
        expected = char
        actual = self.rot13.rot13(char, self.lower_start, self.lower_end)
        self.assertTrue(expected == actual, 'Actual is not None')

    def test_urlencode(self):
        raw_url = "string\nstring"
        url = urllib.quote(raw_url)
        print "Encoded url: "  + str(url)
        url = urllib.unquote(url)
        print "UnEncoded url: "  + str(url)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()