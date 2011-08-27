class ApiResultPrettyPrintable:
    def __init__(self, styler):
        self.__dict__.update(locals())

    def toString(self, apiResult):
        if apiResult.http_status == 200:
            color = 'green'
        elif apiResult.http_status == 202:
            color = 'yellow'
        else:
            color = 'red'

        status_str = "%s %s %s" % (apiResult.http_version, str(apiResult.http_status), apiResult.http_reason)
        headers_str = '\n'.join(['%s: %s' % (k, v) for k, v in apiResult.headers]) + '\n'

        full_str = "%s\n%s\n%s" % (self.styler.color(status_str, color), self.styler.color(headers_str, 'purple'), apiResult.body)
        return full_str.strip()

class ApiResult:
    def __init__(self, request_url, http_response, headers, body, stringizer = None):
        self.http_status  = http_response.status
        self.http_reason  = http_response.reason
        self.http_version = ('HTTP/1.0' if http_response.version == 10 else 'HTTP/1.1')
        self.__dict__.update(locals())
    def __str__(self):
        if self.stringizer:
            return self.stringizer.toString(self)
        return repr(self)

class Factory:
    def __init__(self, stringizer):
        self.__dict__.update(locals())
    def create(self, url_secure, response, headers, body):
        return ApiResult(url_secure, response, headers, body, self.stringizer)

class FactoryFactory:
    def create(self, stringizer = None):
        return Factory(stringizer)       
