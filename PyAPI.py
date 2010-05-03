from PyAPIBundles import PyAPIBundles
from PyAPIFilters import PyAPIFilters
from RequestGenerator import RequestGenerator
from PyAPIResults import PyAPIResults
import http.client

class PyAPI:

    def __init__(self, api_id, secret, host, port):
        self.api_id = api_id
        self.secret = secret
        self.host   = host
        self.port   = port

    def cons_getConstituentsById(self, cons_ids, filters=None, bundles=None):
        query_str = 'cons_ids=' + ','.join([str(elem) for elem in cons_ids])

        if filters:
            f = PyAPIFilters(filters)
            query_str += '&filter=' + str(f)

        if bundles:
            b = PyAPIBundles(bundles)
            query_str += '&bundles=' + str(b)

        url_secure = self._generateRequest('/cons/get_constituents_by_id', query_str)
        return self._makeGETRequest(url_secure)

    def circle_listCircles(self, circle_type=None, state_cd=None):
        query_str = ''

        if circle_type:
            query_str += 'circle_type=' + str(circle_type)

        if state_cd:
            query_str += '&state_cd=' + str(state_cd)

        url_secure = self._generateRequest('/circle/list_circles', query_str)
        return self._makeGETRequest(url_secure)

    def _generateRequest(self, api_call, api_params):
        host = self.host
        if self.port != 80:
            host = host + ":" + self.port

        request = RequestGenerator(self.api_id, self.secret, self.host)
        url_secure = request.getUrl(api_call, api_params)
        return url_secure

    def _makeGETRequest(self, url_secure):
        connection = http.client.HTTPConnection(self.host, self.port)
        connection.request('GET', url_secure.getPathAndQuery())

        response = connection.getresponse()
        headers = response.getheaders()
        body = response.read().decode()

        connection.close()

        results = PyAPIResults(response, headers, body)
        return results

    def _makePOSTRequest(self, url_secure):
        pass