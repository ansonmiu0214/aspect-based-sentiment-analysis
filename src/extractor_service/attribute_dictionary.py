import spacy


def is_similar(model, attr1, attr2, threshold):
    tokens = model(' '.join([attr1, attr2]))
    similarity = tokens[0].similarity(tokens[1])
    return similarity >= threshold


class AttributeDictionary():
    def __init__(self, attrs: list = None, radius=0.78, model=spacy.load("en_core_web_md")):
        self.size = len(attrs)
        self.attrs = attrs
        self.radius = radius
        # TODO:Change the threshold to argument
        self.threshold = 0.7
        self.category = "country"
        self.model = model

    def reduce_dict(self, new_radius=0):
        # Assign new radius value.
        if new_radius >= self.radius:
            self.radius = new_radius
        skip_set = set()

        for i in range(self.size):
            for j in range(i, self.size):
                if is_similar(self.model, self.attrs[i], self.attrs[j], self.threshold):
                    skip_set.add(j)
        for x in skip_set:
            self.attrs.delete(x)

    def add_attr(self, new_attr):
        self.attrs.append(new_attr)

    def validate_attr(self, new_attr):
        for attr in self.attrs:
            if is_similar(self.model, attr, new_attr, self.threshold):
                return True
        return False

    def initialise(self, data_path):
        pass


class KnowledgeModel():
    def __init__(self):
        self.ent_dict = dict()

    def add_dict(self, attr_dict: AttributeDictionary):
        self.ent_dict[attr_dict.category] = attr_dict


ATTRS = ['economy', 'display']
if __name__ == '__main__':
    attr_dict = AttributeDictionary(attrs=ATTRS)
    if attr_dict.validate_attr('finance'):
        print('Hahaha')
    else:
        print("Sorry it is too low for the similarity. ")
