#!/home/sfrazer/bin/python

from optparse import OptionParser
import http.client
import sys
from xml.dom import minidom
import configparser
from URL import URL
from RequestGenerator import RequestGenerator

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    version = "BSD PyAPI 1.0"

    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-v", "--verbose",
                      dest="verbose",
                      help="Makes this tool loud and obnoxious.",
                      action="store_true",
                      default=False)

    parser.add_option("-f", "--file",
                      dest="config_file",
                      help="The Configuration File",
                      default='/etc/bsdapi')

    (options, args) = parser.parse_args()

    api_call = args[0]
    api_params = args[1]

    config = configparser.RawConfigParser()
    config.read(options.config_file)

    settings = {'basic' : {'host': 'localhost', 'port': '80'}}

    for key, value in config.items('basic'):
        settings['basic'][key] = value

    host = settings['basic']['host']
    if settings['basic']['port'] != 80:
        host = host + ":" + settings['basic']['port']

    request = RequestGenerator(settings['basic']['api_id'], settings['basic']['secret'], host)

    connection = http.client.HTTPConnection(settings['basic']['host'], settings['basic']['port'])
    url_secure = request.getUrl(api_call, api_params)

    if options.verbose:
        print(url_secure)

    connection.request('GET', url_secure.getPathAndQuery())
    response = connection.getresponse()

    headers = response.getheaders()
    data = response.read().decode()
    try:
        data_xml = minidom.parseString(data)
        data_xml_formatted = data_xml.toxml()
        data_status = "%sXML Okay%s\n" % (bcolors.OKGREEN, bcolors.ENDC)
    except:
        data_xml_formatted = ''
        data_status = "%sXML Malformed%s\n" % (bcolors.FAIL, bcolors.ENDC)

    http_version = ('HTTP/1.0' if response.version == 10 else 'HTTP/1.1')
    if response.status == 200:
        color = bcolors.OKGREEN
    elif response.status == 202:
        color = bcolors.WARNING
    else:
        color = bcolors.FAIL

    sys.stdout.write("%s%s %s %s%s\n" % (color, http_version, response.status, response.reason, bcolors.ENDC))

    for (key, value) in headers:
        sys.stdout.write( "%s%s: %s%s\n" % (bcolors.HEADER, key, value, bcolors.ENDC))

    sys.stdout.write("\n%s\n\n%s\n" % (data_xml_formatted, data_status))
    connection.close()
