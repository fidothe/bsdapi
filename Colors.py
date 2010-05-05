class Colors:
    def __init__(self):
        self.enable()

    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''

    def enable(self):
        self.PURPLE = '\033[95m'
        self.BLUE = '\033[94m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'

    def docolor(self, string, color):
        return "%s%s%s" % (color, string, self.ENDC)

    def purple(self, string):
        return self.docolor(string, self.PURPLE)

    def blue(self, string):
        return self.docolor(string, self.BLUE)

    def green(self, string):
        return self.docolor(string, self.GREEN)

    def yellow(self, string):
        return self.docolor(string, self.YELLOW)

    def red(self, string):
        return self.docolor(string, self.RED)