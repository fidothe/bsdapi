from BsdApiBundles import BsdApiBundles
from BsdApiFilters import BsdApiFilters
from BsdApiResults import BsdApiResults
from collections import OrderedDict
from RequestGenerator import RequestGenerator
import http.client, urllib.parse
from http.client import HTTPException
import sys
import traceback
import base64

class BsdApi:

    GET = 'GET'
    POST = 'POST'

    def __init__(self, basic_settings, options=None):
        self.api_id = basic_settings['api_id'].strip()
        self.secret = basic_settings['secret'].strip()
        self.host   = basic_settings['host'].strip()
        self.port   = basic_settings['port'].strip()
        self.secure_port = basic_settings['secure_port'].strip()
        self.username = basic_settings['username'].strip()
        self.password = basic_settings['password'].strip()
        self.options = options

    def cons_getConstituents(self, filter, bundles=None):
        query = {'filter': str(BsdApiFilters(filter))}

        if bundles:
            query['bundles'] = str(BsdApiBundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents', query)
        return self._makeGETRequest(url_secure)

    def cons_getConstituentsById(self, cons_ids, filter=None, bundles=None):
        '''Retrieves constituents by ID '''
        query = {'cons_ids': ','.join([str(elem) for elem in cons_ids])}

        if filter:
            query['filter'] =  str(BsdApiFilters(filter))

        if bundles:
            query['bundles'] = str(BsdApiBundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents_by_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getConstituentsByExtId(self, ext_type, ext_ids, filter=None, bundles=None):
        query = {'ext_type': ext_type, 'ext_ids': ','.join([str(elem) for elem in ext_ids])}

        if filter:
            query['filter'] =  str(BsdApiFilters(filter))

        if bundles:
            query['bundles'] = str(BsdApiBundles(bundles))

        url_secure = self._generateRequest('/cons/get_constituents_by_ext_id', query)
        return self._makeGETRequest(url_secure)

    def cons_getUpdatedConstituents(self, changed_since, filter=None, bundles=None):
        query = {'changed_since': str(changed_since)}

        if filter:
            query['filter'] =  str(BsdApiFilters(filter))

        if bundles:
            query['bundles'] = str(BsdApiBundles(bundles))

        url_secure = self._generateRequest('/cons/get_updated_constituents', query)
        return self._makeGETRequest(url_secure)

    def cons_setExtIds(self, ext_type, cons_id__ext_id):
        query = {'ext_type': str(ext_type)}
        query.update(cons_id__ext_id)
        print(query)
        url_secure = self._generateRequest('/cons/set_ext_ids')
        return self._makePOSTRequest(url_secure, query)

    def cons_deleteConstituentsById(self, cons_ids):
        query = {'cons_ids': ','.join([str(cons) for cons in cons_ids])}
        url_secure = self._generateRequest('/cons/delete_constituents_by_id')
        return self._makePOSTRequest(url_secure, query)

    def cons_getBulkConstituentData(self, format, fields, cons_ids=None, filter=None):
        query = {'format': str(format), 'fields': ','.join([str(field) for field in fields])}

        if cons_ids:
            query['cons_ids'] = ','.join([str(cons) for cons in cons_ids])

        if filter:
            query['filter'] =  str(BsdApiFilters(filter))

        url_secure = self._generateRequest('/cons/get_bulk_constituent_data')
        return self._makePOSTRequest(url_secure, query)

    def cons_setConstituentData(self, xml_data):
        url_secure = self._generateRequest('/cons/set_constituent_data')
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_group_listConstituentGroups(self):
        url_secure = self._generateRequest('/cons_group/list_constituent_groups')
        return self._makeGETRequest(url_secure)

    def cons_group_getConstituentGroup(self, cons_group_id):
        query = {'cons_group_id': str(cons_group_id)}
        url_secure = self._generateRequest('/cons_group/get_constituent_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_addConstituentGroup(self, xml_data):
        url_secure = self._generateRequest('/cons/add_constituent_group')
        return self._makePOSTRequest(url_secure, xml_data)

    def cons_group_deleteConstituentGroup(self, cons_group_ids):
        query = {'cons_group_ids': ','.join([str(c) for c in cons_group_ids])}
        url_secure = self._generateRequest('/cons_group/delete_constituent_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_getConsIdsForGroup(self, cons_group_id):
        query = {'cons_group_ids': str(cons_group_id)}
        url_secure = self._generateRequest('/cons_group/get_cons_ids_for_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_getExtIdsForGroup(self, cons_group_id, ext_type):
        query = {'cons_group_ids': str(cons_group_id), 'ext_type': ext_type}
        url_secure = self._generateRequest('/cons_group/get_ext_ids_for_group', query)
        return self._makeGETRequest(url_secure)

    def cons_group_setExtIdsForGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_ids': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/set_ext_ids_for_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_addConsIdsToGroup(self, cons_group_id, cons_ids):
        query = {'cons_group_ids': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/cons_group/add_cons_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_addExtIdsToGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_ids': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/add_ext_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_removeConsIdsToGroup(self, cons_group_id, cons_ids):
        query = {'cons_group_ids': str(cons_group_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/cons_group/remove_cons_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def cons_group_removeExtIdsToGroup(self, cons_group_id, ext_type, ext_ids):
        query = {'cons_group_ids': str(cons_group_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext) for ext in ext_ids])}

        url_secure = self._generateRequest('/cons_group/remove_ext_ids_to_group')
        return self._makePOSTRequest(url_secure, query)

    def circle_listCircles(self, circle_type=None, state_cd=None):
        query = {}

        if circle_type:
            query['circle_type'] = str(circle_type)

        if state_cd:
            query['state_cd'] = str(state_cd)

        url_secure = self._generateRequest('/circle/list_circles', query)
        return self._makeGETRequest(url_secure)

    def circle_getConsIdsForCircle(self, circle_id):
        query = {'circle_id': str(circle_id)}
        url_secure = self._generateRequest('/circle/get_cons_ids_for_circle', query)
        return self._makeGETRequest(url_secure)

    def circle_getExtIdsForCircle(self, circle_id, ext_type):
        query = {'circle_id': str(circle_id), 'ext_type': ext_type}
        url_secure = self._generateRequest('/circle/get_ext_ids_for_circle', query)
        return self._makeGETRequest(url_secure)

    def circle_setConsIdsForCircle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/circle/set_cons_ids_for_circle')
        return self._makeGETRequest(url_secure, query)

    def circle_setExtIdsForCircle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generateRequest('/circle/set_ext_ids_for_circle')
        return self._makePOSTRequest(url_secure, query)

    def circle_addConsIdsForCircle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/circle/add_cons_ids_for_circle')
        return self._makeGETRequest(url_secure, query)

    def circle_addExtIdsForCircle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generateRequest('/circle/add_ext_ids_for_circle')
        return self._makeGETRequest(url_secure, query)

    def circle_removeConsIdsForCircle(self, circle_id, cons_ids):
        query = {'circle_id': str(circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/circle/remove_cons_ids_for_circle')
        return self._makePOSTRequest(url_secure, query)

    def circle_removeExtIdsForCircle(self, circle_id, ext_type, ext_ids):
        query = {'circle_id': str(circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generateRequest('/circle/remove_ext_ids_for_circle')
        return self._makePOSTRequest(url_secure, query)

    def circle_moveConsIdsForCircle(self, from_circle_id, to_circle_id, cons_ids):
        query = {'from_circle_id': str(from_circle_id),
                 'to_circle_id': str(to_circle_id),
                 'cons_ids': ','.join([str(cons) for cons in cons_ids])}

        url_secure = self._generateRequest('/circle/move_cons_ids_for_circle')
        return self._makePOSTRequest(url_secure, query)

    def circle_moveExtIdsForCircle(self, from_circle_id, to_circle_id, ext_type, ext_ids):
        query = {'from_circle_id': str(from_circle_id),
                 'to_circle_id': str(to_circle_id),
                 'ext_type': ext_type,
                 'ext_ids': ','.join([str(ext_id) for ext_id in ext_ids])}

        url_secure = self._generateRequest('/circle/move_ext_ids_for_circle')
        return self._makePOSTRequest(url_secure, query)

    def circle_setCircleAdministrator(self, circle_id, cons_id):
        query = {'circle_id': str(from_circle_id),
                 'cons_id': str(to_circle_id)}

        url_secure = self._generateRequest('/circle/set_circle_administrator')
        return self._makePOSTRequest(url_secure, query)

    def circle_demoteCircleAdministrator(self, circle_id, cons_id):
        query = {'circle_id': str(from_circle_id),
                 'cons_id': str(to_circle_id)}

        url_secure = self._generateRequest('/circle/demote_circle_administrator')
        return self._makePOSTRequest(url_secure, query)

    def circle_setCircleOwner(self, circle_id, cons_id):
        query = {'circle_id': str(from_circle_id),
                 'cons_id': str(to_circle_id)}

        url_secure = self._generateRequest('/circle/set_circle_owner')
        return self._makePOSTRequest(url_secure, query)

    def outreach_getPageById(self, id):
        query = {'id': str(id)}
        url_secure = self._generateRequest('/outreach/get_page_by_id')
        return self._makePOSTRequest(url_secure, query)

    def outreach_setPageData(self, xml_data):
        url_secure = self._generateRequest('/outreach/set_page_data', {})
        return self._makePOSTRequest(url_secure, xml_data)

    def signup_processSignup(self, xml_data):
        query = {}
        url_secure = self._generateRequest('/signup/process_signup', query)
        return self._makePOSTRequest(url_secure, xml_data)

    def signup_listForms(self):
        query = {}
        url_secure = self._generateRequest('/signup/list_forms', query)
        return self._makeGETRequest(url_secure)

    def signup_listFormFields(self, signup_form_id):
        query = {'signup_form_id': str(signup_form_id)}
        url_secure = self._generateRequest('/signup/list_form_fields', query)
        return self._makeGETRequest(url_secure)

    def signup_signupCount(self, signup_form_id, signup_form_field_ids=None):
        query = {'signup_form_id': str(signup_form_id)}

        if signup_form_field_ids:
            query['signup_form_field_ids'] = ','.join([str(elem) for elem in signup_form_field_ids])

        url_secure = self._generateRequest('/signup/signup_count', query)
        return self._makeGETRequest(url_secure)

    def signup_countByField(self, signup_form_id, signup_form_field_id):
        query = {'signup_form_id': str(signup_form_id),
                 'signup_form_field_id': str(signup_form_field_id)}

        url_secure = self._generateRequest('/signup/count_by_field', query)
        return self._makeGETRequest(url_secure)

    def wrappers_listWrappers(self):
        url_secure = self._generateRequest('/wrappers/list_wrappers')
        return self._makeGETRequest(url_secure)

    def account_checkCredentials(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generateRequest('/account/check_credentials', query, https = True)
        return self._makeGETRequest(url_secure, https = True)

    def account_createAccount(self, email, password, firstname, lastname, zip):
        query = {'email':email, 'password':password, 'firstname':firstname, 'lastname':lastname, 'zip':zip}
        url_secure = self._generateRequest('/account/create_account', query, https = True)
        return self._makeGETRequest(url_secure, https = True)

    def account_resetPassword(self, userid):
        query = {'userid': userid}
        url_secure = self._generateRequest('/account/reset_password', query, https = True)
        return self._makeGETRequest(url_secure, https = True)

    def account_setPassword(self, userid, password):
        query = {'userid': userid, 'password': password}
        url_secure = self._generateRequest('/account/set_password', query, https = True)
        return self._makeGETRequest(url_secure, https = True)

    def getDeferredResults(self, deferred_id):
        query = {'deferred_id': deferred_id}
        url_secure = self._generateRequest('/get_deferred_results', query)
        return self._makeGETRequest(url_secure)

    def doRequest(self, api_call, api_params = {}, request_type = GET, body = None, headers = None, https = False):
        url = self._generateRequest(api_call, api_params, https)
        return self._makeRequest(url, request_type, body, headers, https)

    def _makeRequest(self, url_secure, request_type, http_body = None, headers = None, https=False):
        connect_function = http.client.HTTPSConnection if https else http.client.HTTPConnection
        port = self.secure_port if https else self.port

        connection = connect_function(self.host, port)
        if(self.options.verbose):
            connection.set_debuglevel(5)
        if self.username:
            auth_string = self.username
            if self.password:
                auth_string += ":" + self.password
            if headers == None:
                headers = dict()
            headers["Authorization"] = "Basic " + base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        if http_body != None and headers != None:
            connection.request(request_type, url_secure.getPathAndQuery(), http_body, headers)
        elif headers != None:
            connection.request(request_type, url_secure.getPathAndQuery(), None, headers)
        else:
            connection.request(request_type, url_secure.getPathAndQuery())
        response = None
        try:
            response = connection.getresponse()
            headers = response.getheaders()
            body = response.read().decode()

            connection.close()

            results = BsdApiResults(url_secure, response, headers, body, self.options)
            return results
        except HTTPException:
            print(''.join(traceback.format_exception(*sys.exc_info())))
            print("Error calling " + url_secure.getPathAndQuery())

    def _generateRequest(self, api_call, api_params = {}, https = False):
        host = self.host

        if https:
            if self.secure_port != 443:
                host = host + ':' + self.secure_port
        else:
            if self.port != 80:
                host = host + ":" + self.port

        request = RequestGenerator(self.api_id, self.secret, host, https)
        url_secure = request.getUrl(api_call, api_params)
        return url_secure

    def _makeGETRequest(self, url_secure, https = False):
        return self._makeRequest(url_secure, BsdApi.GET, https = https);

    def _makePOSTRequest(self, url_secure, body, https = False):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/xml"}

        if type(body).__name__ == 'dict':
            http_body = urllib.parse.urlencode(body)
        else:
            http_body = body

        return self._makeRequest(url_secure, BsdApi.POST, http_body, headers, https)
