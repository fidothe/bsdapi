#!/home/sfrazer/bin/python
import hmac, hashlib, unittest
from time import time
from URL import URL
import http.client

class RequestGenerator:

    def __init__(self, api_id, api_secret, api_host):
        self.api_secret = api_secret
        self.api_id     = api_id
        self.api_host   = api_host
        self.api_base   = '/page/api'

    def gen_query_str(self, api_ts, api_params):
        query = 'api_ver=1&api_id=' + self.api_id + '&api_ts=' + str(api_ts)
        if api_params:
            query = api_params + '&' + query
        return query

    def gen_signing_string(self, api_ts, api_call, api_params):
        string = "\n".join([self.api_id, str(api_ts), self.api_base + api_call, self.gen_query_str(api_ts, api_params)])
        return hmac.new(self.api_secret.encode(), string.encode(), hashlib.sha1).hexdigest()

    def getUrl(self, api_call, api_params):
        unix_ts = int(time())
        signing_string = self.gen_signing_string(unix_ts, api_call, api_params)

        url = URL()
        url.host = self.api_host
        url.path = self.api_base + api_call
        url.query = self.gen_query_str(unix_ts, api_params) + '&api_mac=' + signing_string
        return url

class TestRequestGenerator(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'
        self.secret = '7405d35963605dc36702c06314df85db7349613f'
        self.api_id = 'sfrazer'

    def test_hmacGenerateProperlyWhenAPIHasNoParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request.gen_signing_string('1272659462', '/circle/list_circles', '')
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

    def test_hmacGenerateProperlyWhenAPIHasParams(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request.gen_signing_string('1272662274', '/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')
        self.assertEqual(signing_string, 'c2af877085bcb5390aed0c8256b14ad05f2e3ef1')

    def test_urlWithHMACDoesntGenerate403(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl('/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')
        response = self.doHTTPGetRequestAndGetResponse(url_secure)
        self.assertNotEqual(response.status, 403)

    def test_urlWithHMACDoesntGenerate403_2(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl('/circle/list_circles', '')
        response = self.doHTTPGetRequestAndGetResponse(url_secure)
        self.assertNotEqual(response.status, 403)

    def test_urlWithHMACDoesntGenerate403WhenParamsHasAFilter(self):
        request = RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl('/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5&filter=state_cd=(CA,MA),is_subscribed')
        response = self.doHTTPGetRequestAndGetResponse(url_secure)
        self.assertNotEqual(response.status, 403)

    def doHTTPGetRequestAndGetResponse(self, url_secure):
        connection = http.client.HTTPConnection(self.host)
        connection.request('GET', url_secure.getPathAndQuery())
        response = connection.getresponse()
        connection.close()
        return response

if __name__ == '__main__':
    unittest.main()