import unittest
import http.client
import urllib.parse

class URL:

    def __init__(self):
        self.protocol = 'http'
        self.host = 'localhost'
        self.path = '/'
        self.query = ''

    def __setattr__(self, name, val):
        if name not in ['protocol', 'host', 'path', 'query']:
            raise URLError('Cannot set that value')

        if name == 'query' and type(val).__name__ == 'dict':
            self.__dict__[name] = urllib.parse.urlencode(val)
        elif name == 'query' and type(val).__name__ == 'str':
            self.__dict__[name] = val
        elif name == 'path' and val[0] != '/':
            self.__dict__[name] = '/' + val
        else:
            self.__dict__[name] = val

    def __str__(self):
        url = self.protocol + '://' + self.host + self.path
        if len(self.query):
            url = url + '?' + self.query
        return url

    def getPathAndQuery(self):
        url = self.path
        if len(self.query):
            url = url + '?' + self.query
        return url

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'

    def test_GenerateProperURLWithAllElements(self):
        url = URL()
        url.protocol = 'http'
        url.host = 'test.com'
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingProtocol(self):
        url = URL()
        url.host = 'test.com'
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingHost(self):
        url = URL()
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')
    
    def test_GenerateProperURLWithQueryHash(self):
        url = URL()
        url.path = '/a/b/c'
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingPath(self):
        url = URL()
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/?a=1&b=2')
    
    def test_GenerateProperURLWhenPathDoesntStartWithASlash(self):
        url = URL()
        url.path = 'a/b/c'
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWhenAllParamsArentSet(self):
        url = URL()
        self.assertEqual(str(url), 'http://localhost/')

if __name__ == '__main__':
    unittest.main()
