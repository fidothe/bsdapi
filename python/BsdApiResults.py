from Colors import Colors

class BsdApiResults:

    def __init__(self, request_url, http_response, headers, body, options=None):
        self.http_status  = http_response.status
        self.http_reason  = http_response.reason
        self.http_version = ('HTTP/1.0' if http_response.version == 10 else 'HTTP/1.1')
        self.headers      = headers
        self.body         = body
        self.request_url  = request_url
        self.options      = options

    def __str__(self):
        color = Colors()

        if type(self.options).__name__ == 'NoneType' or not self.options.color:
            color.disable()

        if self.http_status == 200:
            status_func = color.green
        elif self.http_status == 202:
            status_func = color.yellow
        else:
            status_func = color.red

        status_str = "%s %s %s" % (self.http_version, str(self.http_status), self.http_reason)

        headers_str = ''
        for (key, value) in self.headers:
            headers_str += "%s: %s\n" % (key, value)

        full_str = "%s\n%s\n%s" % (status_func(status_str), color.purple(headers_str), self.body)
        return full_str.strip()
