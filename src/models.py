import abc
from typing import List


##############
# Models
##############

class HasMetadata(abc.ABC):
    def __init__(self):
        self.metadata = dict()

    def add_metadata(self, key, value):
        self.metadata[key] = value


class Document(HasMetadata):
    def __init__(self):
        super().__init__()
        self.components = []  # type: List[DocumentComponent]
        self.entities = []  # type: List[EntityEntry]

    def add_component(self, component):
        self.components.append(component)

    def add_entity(self, entity):
        self.entities.append(entity)


class DocumentComponent:
    def __init__(self, type, text):
        self.type = type  # type: str
        self.text = text  # type: str


class EntityEntry:
    def __init__(self, name):
        self.name = name
        self.attributes = []  # type: List[AttributeEntry]

    def add_attribute(self, attribute):
        '''
        :param attribute: AttributeEntry
        :return: void
        '''
        self.attributes.append(attribute)


class AttributeEntry(HasMetadata):
    def __init__(self, attribute, expression, sentiment=None):
        super().__init__()
        self.attribute = attribute  # type: str
        self.expression = expression  # type: str
        self.sentiment = sentiment  # type: float

    def __repr__(self):
        truncate = lambda n, x: x[:n] + "..."
        max_length = 10
        return "Attr={} Exprs={} Sent={}".format(self.attribute,
                                                 list(map(lambda x: truncate(max_length, x), self.expression)),
                                                 self.sentiment)


class Query:
    def __init__(self, entity, attribute, positive_sentiment):
        self.entity = entity
        self.attribute = attribute
        self.positive_sentiment = positive_sentiment


##############
# Strategies
##############

class PreprocessorService(abc.ABC):
    @abc.abstractmethod
    def preprocess(self, doc):
        '''

        :param doc:
        :rtype: Document
        '''
        pass


class ExtractorService(abc.ABC):
    @abc.abstractmethod
    def extract(self, doc: Document) -> Document:
        '''

        :param doc:
        :rtype: Document
        '''
        pass


class SentimentService(abc.ABC):
    @abc.abstractmethod
    def compute_sentiment(self, text):
        '''

        :param text: str
        :rtype: float
        '''
        pass


class QueryParser(abc.ABC):
    @abc.abstractmethod
    def parse_query(self, text) -> Query:
        '''


        :param text:
        :rtype: Query
        '''
        pass


class DataSourceService(abc.ABC):
    @abc.abstractmethod
    def process_document(self, document: Document):
        '''

        :param document:
        :return:
        '''
        pass

    @abc.abstractmethod
    def lookup(self, query: Query) -> List[AttributeEntry]:
        '''

        :param query:
        :return:
        '''
        pass


class AggregatorService(abc.ABC):
    @abc.abstractmethod
    def aggregate_sentiment(self, sentiments):
        '''

        :param sentiments: [float]
        :rtype: float
        '''
        pass
