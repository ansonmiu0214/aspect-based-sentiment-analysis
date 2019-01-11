import json

import spacy


def is_similar(model, attr1, attr2, threshold):
    tokens = model(' '.join([attr1, attr2]))
    similarity = tokens[0].similarity(tokens[1])
    # print(similarity)
    return similarity >= threshold


class AttributeDictionary():
    def __init__(self, attrs: list = None, radius=0.78, threshold=0.65):
        self.size = len(attrs)
        self.attrs = attrs
        self.radius = radius
        self.threshold = threshold

    def reduce_dict(self, new_radius=0, model=None):

        if model is None:
            raise Exception("Model is required")
        # Assign new radius value.
        if new_radius >= self.radius:
            self.radius = new_radius
        skip_set = set()

        for i in range(self.size):
            for j in range(i, self.size):
                if is_similar(model, self.attrs[i], self.attrs[j], self.threshold):
                    skip_set.add(j)
        for x in skip_set:
            self.attrs.delete(x)

    def add_attr(self, new_attr):
        self.attrs.append(new_attr)

    def validate_attr(self, new_attr, model):
        for attr in self.attrs:
            if is_similar(model, attr, new_attr, self.threshold):
                return True
        return False

    def initialise(self, data_path):
        pass


class KnowledgeModel():
    def __init__(self, model = spacy.load("en_core_web_md")):
        self.ent_dict = dict()
        self.model = model

    def add_dict(self, new_attr_dict: AttributeDictionary, new_category):
        self.ent_dict[new_category] = new_attr_dict

    def validate(self, category, attr):
        if category in self.ent_dict:
            attr_dict = self.ent_dict[category]
            return attr_dict.validate_attr(attr, self.model)
        return True
