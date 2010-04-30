import bsdapi
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_hmac(self):
        request = bsdapi.RequestGenerator('sfrazer', '7405d35963605dc36702c06314df85db7349613f')
        request.set_url('http://enoch.bluestatedigital.com:17260/page/api/circle/list_circles')
        signing_string = request.gen_signing_string('1272659462')
        self.assertEqual(signing_string, '13e9de81bbdda506b6021579da86d3b6edea9755')

if __name__ == '__main__':
    unittest.main()