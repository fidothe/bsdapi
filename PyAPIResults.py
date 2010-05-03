from bcolors import bcolors

class PyAPIResults:

    def __init__(self, http_response, headers, body):
        self.http_status  = http_response.status
        self.http_reason  = http_response.reason
        self.http_version = ('HTTP/1.0' if http_response.version == 10 else 'HTTP/1.1')
        self.headers      = headers
        self.body         = body

    def prettyPrint(self):
        if self.http_status == 200:
            color = bcolors.OKGREEN
        elif self.http_status == 202:
            color = bcolors.WARNING
        else:
            color = bcolors.FAIL

        s = "%s%s %s %s%s\n" % (color, self.http_version, self.http_status, self.http_reason, bcolors.ENDC)

        for (key, value) in self.headers:
            s += "%s%s: %s%s\n" % (bcolors.HEADER, key, value, bcolors.ENDC)

        s += "\n%s\n" % (self.body)
        return s

    def __str__(self):
        s = "%s %s %s\n" % (self.http_version, str(self.http_status), self.http_reason)

        for (key, value) in self.headers:
            s += "%s: %s\n" % (key, value)

        s += "\n"
        s += self.body
        return s