#!/home/sfrazer/bin/python

from os.path import exists
from optparse import OptionParser
import http.client
import sys, code, configparser, readline, atexit, os, rlcompleter
from xml.dom import minidom
from URL import URL
from RequestGenerator import RequestGenerator
from BsdApi import BsdApi

class Console(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>",
                       histfile=os.path.expanduser("~/.pyapi_history")):
        self.usage = "Usage: %prog [options]"
        self.version = "BSD Interactive API 1.0"

        self.parser = OptionParser(usage=self.usage, version=self.version)

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

        if not exists(self.options.config_file):
            sys.stderr.write("Error: Config file %s does not exist\n" % (self.options.config_file) % ", either add it or use -f <path_to_config_file>" )
            sys.exit(1)

        config = configparser.RawConfigParser()
        config.read(self.options.config_file)

        self.settings = {'basic' : {'host': 'localhost', 'port': '80'}}

        for key, value in config.items('basic'):
            self.settings['basic'][key] = value

        self.api = BsdApi(self.settings['basic']['api_id'], self.settings['basic']['secret'], self.settings['basic']['host'], self.settings['basic']['port'], self.options)

        code.InteractiveConsole.__init__(self, self.__dict__)
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.write_history_file(histfile)

    def run(self):
        sys.ps1 = 'api> '
        self.interact('BSD Interactive API')

if __name__ == '__main__':
    console = Console()
    console.run()
