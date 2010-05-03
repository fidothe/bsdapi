import bsdapi
import unittest
import http.client

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.host = 'enoch.bluestatedigital.com:17260'
        self.secret = '7405d35963605dc36702c06314df85db7349613f'
        self.api_id = 'sfrazer'

    def test_hmacGenerateProperlyWhenAPIHasNoParams(self):
        request = bsdapi.RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request.gen_signing_string('1272659462', '/circle/list_circles', '')
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

    def test_hmacGenerateProperlyWhenAPIHasParams(self):
        request = bsdapi.RequestGenerator(self.api_id, self.secret, self.host)
        signing_string = request.gen_signing_string('1272662274', '/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')
        self.assertEqual(signing_string, 'c2af877085bcb5390aed0c8256b14ad05f2e3ef1')

    def test_urlWithHMACDoesntGenerate403(self):
        request = bsdapi.RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl('/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')
        response = self.doHTTPGetRequestAndGetResponse(url_secure)
        self.assertNotEqual(response.status, 403)

    def test_urlWithHMACDoesntGenerate403_2(self):
        request = bsdapi.RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl('/circle/list_circles', '')
        response = self.doHTTPGetRequestAndGetResponse(url_secure)
        self.assertNotEqual(response.status, 403)

    def test_urlWithHMACDoesntGenerate403WhenParamsHasAFilter(self):
        request = bsdapi.RequestGenerator(self.api_id, self.secret, self.host)
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
