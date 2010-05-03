import bsdapi
import unittest
import http.client

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'

    def test_GenerateProperURLWithAllElements(self):
        url = bsdapi.URL()
        url.protocol = 'http'
        url.host = 'test.com'
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingProtocol(self):
        url = bsdapi.URL()
        url.host = 'test.com'
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://test.com/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingHost(self):
        url = bsdapi.URL()
        url.path = '/a/b/c'
        url.query = 'a=1&b=2'
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')
    
    def test_GenerateProperURLWithQueryHash(self):
        url = bsdapi.URL()
        url.path = '/a/b/c'
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWithMissingPath(self):
        url = bsdapi.URL()
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/?a=1&b=2')
    
    def test_GenerateProperURLWhenPathDoesntStartWithASlash(self):
        url = bsdapi.URL()
        url.path = 'a/b/c'
        url.query = {'a': 1, 'b': 2}
        self.assertEqual(str(url), 'http://localhost/a/b/c?a=1&b=2')

    def test_GenerateProperURLWhenAllParamsArentSet(self):
        url = bsdapi.URL()
        self.assertEqual(str(url), 'http://localhost/')

if __name__ == '__main__':
    unittest.main()
