from PyAPIBundles import PyAPIBundles
from PyAPIFilters import PyAPIFilters
from RequestGenerator import RequestGenerator
from PyAPIResults import PyAPIResults
import http.client
import urllib.parse
from collections import OrderedDict

class PyAPI:

    def __init__(self, api_id, secret, host, port):
        self.api_id = api_id
        self.secret = secret
        self.host   = host
        self.port   = port

    def cons_getConstituentsById(self, cons_ids, filters=None, bundles=None):
        query = {'cons_ids': ','.join([str(elem) for elem in cons_ids])}

        if filters:
            query['filter'] =  str(PyAPIFilters(filters))

        if bundles:
            query['bundles'] = str(PyAPIBundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents_by_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getConstituentsByExtId(self, ext_type, ext_ids, filters=None, bundles=None):
        query = {'ext_type': ext_type, 'ext_ids': ','.join([str(elem) for elem in ext_ids])}

        if filters:
            f = PyAPIFilters(filters)
            query['filter'] =  str(f)

        if bundles:
            b = PyAPIBundles(bundles)
            query['bundles'] = str(b)

        url_secure = self._generateRequest('/cons/get_constituents_by_ext_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getUpdatedConstituents(self, changed_since, filters=None, bundles=None):
        query = {'changed_since': str(changed_since)}

        if filters:
            query['filter'] =  str(PyAPIFilters(filters))

        if bundles:
            query['bundles'] = str(PyAPIBundles(bundles))

        url_secure = self._generateRequest('/cons/get_updated_constituents', query)
        return self._makeGETRequest(url_secure)

    def cons_setExtIds(self, ext_type, cons_id__ext_id):
        query = OrderedDict([('ext_type', str(ext_type))])
        query.update(cons_id__ext_id);
        url_secure = self._generateRequest('/cons/set_ext_ids')
        return self._makePOSTRequest(url_secure, urllib.parse.urlencode(query))

    def circle_listCircles(self, circle_type=None, state_cd=None):
        query = {}

        if circle_type:
            query['circle_type'] = str(circle_type)

        if state_cd:
            query['state_cd'] = str(state_cd)

        url_secure = self._generateRequest('/circle/list_circles', query)
        return self._makeGETRequest(url_secure)

    def _generateRequest(self, api_call, api_params = {}):
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

    def _makePOSTRequest(self, url_secure, body):
        connection = http.client.HTTPConnection(self.host, self.port)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/xml"}
        connection.request('POST', url_secure.getPathAndQuery(), body, headers)
        print(url_secure)
        print(body)
        response = connection.getresponse()
        headers = response.getheaders()
        body = response.read().decode()

        connection.close()

        results = PyAPIResults(response, headers, body)
        return results