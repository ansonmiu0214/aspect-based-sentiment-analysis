import abc
from typing import List


##############
# Models
##############

class HasMetadata(abc.ABC):
    '''
    An abstract base class that allows the storing of key/value pairs as metadata.
    '''

    def __init__(self):
        self.metadata = dict()

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def remove_metadata(self, key):
        del self.metadata[key]

    def lookup_metadata(self, key):
        return self.metadata[key]


class Document(HasMetadata):
    '''
    A Document is built with a list of DocumentComponent objects.
    The extractor_service will annotate the Document with EntityEntry objects.
    A Document can also contain metadata (e.g. name, author, source).
    '''
    def __init__(self):
        super().__init__()
        self.components = []  # type: List[DocumentComponent]
        self.entities = []  # type: List[EntityEntry]

    def add_component(self, component):
        self.components.append(component)

    def add_entity(self, entity):
        self.entities.append(entity)


class DocumentComponent:
    '''
    A wrapper around the actual document content.
    The `type` field allows you to store structural information (e.g. heading, table).
    '''
    def __init__(self, type, text):
        self.type = type  # type: str
        self.text = text  # type: str


class EntityEntry(HasMetadata):
    '''
    Each entity has a name (e.g. Apple) and a list of AttributeEntry objects.
    An EntityEntry can also contain metadata (e.g. child entities?)
    '''
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.attributes = []  # type: List[AttributeEntry]

    def add_attribute(self, attribute):
        '''
        :param attribute: AttributeEntry
        :return: void
        '''
        self.attributes.append(attribute)

    def __repr__(self):
        return self.name


class AttributeEntry(HasMetadata):
    '''
    Each AttributeEntry must contain the attribute name and the linguistic expression.
    Sentiment values can be optionally added (depending on the approach).
    An AttributeEntry can also contain metadata (e.g. the document it is from).
    '''
    def __init__(self, attribute, expressions, sentiment=None):
        super().__init__()
        self.attribute = attribute  # type: str
        self.expressions = expressions  # type: List[str]
        self.sentiment = sentiment  # type: float

    def __repr__(self):
        truncate = lambda n, x: x[:n] + "..."
        max_length = 10
        return "Attr={} Exprs={} Sent={}".format(self.attribute,
                                                 list(map(lambda x: truncate(max_length, x), self.expressions)),
                                                 self.sentiment)


class Query:
    '''
    A wrapper class for user queries into the ABSA service.
    '''
    def __init__(self, entity, attribute, positive_sentiment=None):
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
        Given a document (of any kind), adapts it to a Document object.

        :param doc:
        :rtype: Document
        '''
        pass


class ExtractorService(abc.ABC):
    @abc.abstractmethod
    def extract(self, doc: Document) -> Document:
        '''
        Extracts the entity/attribute pairs from the Document object.
        Performs sentiment analysis using the embedded service.
        Annotates the Document object with the extractedEntityEntry objects.
        Returns the annotated Document.

        :param doc:
        :rtype: Document
        '''
        pass


class SentimentService(abc.ABC):
    @abc.abstractmethod
    def compute_sentiment(self, text):
        '''
        Given an input string, returns the sentiment score normalised between [-1, 1].
        -1 denotes negative sentiment.
        (+)1 denotes positive sentiment.

        :param text: str
        :rtype: float
        '''
        pass


class QueryParser(abc.ABC):
    @abc.abstractmethod
    def parse_query(self, text) -> Query:
        '''
        Given an input string, parses it into a Query object.
        The Query must specify the Entity, and the Attribute / Sentiment are optional.

        :param text:
        :rtype: Query
        '''
        pass


class DataSourceService(abc.ABC):
    @abc.abstractmethod
    def process_document(self, document: Document):
        '''
        Processes the Document object into the persistent storage solution used by the implementer.

        :param document:
        :return:
        '''
        pass

    @abc.abstractmethod
    def lookup(self, query: Query) -> List[AttributeEntry]:
        '''
        Given a Query, returns the relevant AttributeEntry objects from the data source.

        :param query:
        :return:
        '''
        pass


class AggregatorService(abc.ABC):
    @abc.abstractmethod
    def aggregate_sentiment(self, sentiments):
        '''
        Given a list of sentiment values (as `float` values), return an aggregate score.

        :param sentiments: [float]
        :rtype: float
        '''
        pass
