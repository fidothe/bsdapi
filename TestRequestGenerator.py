import bsdapi
import unittest
import http.client

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_hmacGenerateProperlyWhenAPIHasNoParams(self):
        request = bsdapi.RequestGenerator('sfrazer', '7405d35963605dc36702c06314df85db7349613f', 'enoch.bluestatedigital.com:17260')
        signing_string = request.gen_signing_string('1272659462', '/circle/list_circles', '')
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

    def test_hmacGenerateProperlyWhenAPIHasParams(self):
        request = bsdapi.RequestGenerator('sfrazer', '7405d35963605dc36702c06314df85db7349613f', 'enoch.bluestatedigital.com:17260')
        signing_string = request.gen_signing_string('1272662274', '/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')
        self.assertEqual(signing_string, 'c2af877085bcb5390aed0c8256b14ad05f2e3ef1')

    def test_urlWithHMACDoesntGenerate403(self):
        request = bsdapi.RequestGenerator('sfrazer', '7405d35963605dc36702c06314df85db7349613f', 'enoch.bluestatedigital.com:17260')
        url_secure = request.full_url('/cons/get_constituents_by_id', 'cons_ids=1,2,3,4,5')

        connection = http.client.HTTPConnection('enoch.bluestatedigital.com:17260')
        connection.request('GET', url_secure)
        response = connection.getresponse()
        connection.close()

        self.assertNotEqual(response.status, 403)

if __name__ == '__main__':
    unittest.main()