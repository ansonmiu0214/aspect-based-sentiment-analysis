class EntityEntry:
    def __init__(self, name):
        self.name = name
        self.attributes = []

    def add_attribute(self, attribute):
        '''
        :param attribute: AttributeEntry
        :return: void
        '''
        self.attributes.append(attribute)


class AttributeEntry:
    def __init__(self, attribute, expression):
        self.attribute = attribute
        self.expression = expression
        self.metadata = dict()

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def __repr__(self):
        return "attr={} expr={}".format(self.attribute, self.expression)
