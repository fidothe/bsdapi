#!/home/sfrazer/bin/python

from os.path import exists
from optparse import OptionParser
import http.client
import sys, code, configparser
from xml.dom import minidom
from URL import URL
from RequestGenerator import RequestGenerator
from PyAPI import PyAPI

class Console:
    def __init__(self):
        usage = "Usage: %prog [options]"
        version = "BSD Interactive API 1.0"

        self.parser = OptionParser(usage=usage, version=version)

        self.parser.add_option("-v", "--verbose",
                               dest="verbose",
                               help="Makes this tool loud and obnoxious.",
                               action="store_true",
                               default=False)

        self.parser.add_option("-c", "--color",
                               dest="color",
                               help="Use ANSI colors for display",
                               action="store_true",
                               default=False)

        self.parser.add_option("-f", "--file",
                               dest="config_file",
                               help="The Configuration File",
                               default='/etc/bsdapi')

        (self.options, self.args) = self.parser.parse_args()
    
    def run(self):
        if not exists(self.options.config_file):
            sys.stderr.write("Error: Config file %s does not exist\n" % (options.config_file) )
            sys.exit(1)

        config = configparser.RawConfigParser()
        config.read(self.options.config_file)

        settings = {'basic' : {'host': 'localhost', 'port': '80'}}

        for key, value in config.items('basic'):
            settings['basic'][key] = value

        api = PyAPI(settings['basic']['api_id'], settings['basic']['secret'], settings['basic']['host'], settings['basic']['port'], self.options)

        local_vars = locals()
        local_vars.update(self.__dict__)

        sys.ps1 = 'api> '
        code.interact('BSD Interactive API', local=local_vars)

if __name__ == '__main__':
    console = Console()
    console.run()