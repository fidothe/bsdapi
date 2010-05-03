class PyAPIFilters:

    def __init__(self, filters):
        self.filters = filters

    def __str__(self):
        return ','.join(self.filters)