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


class HasText(abc.ABC):
    '''
    An abstract base class that stores the text of a token.
    '''

    def __init__(self, text):
        self.text = text


class Document(HasMetadata):
    '''
    A Document is built with a list of DocumentComponent objects.
    The extractor_service will annotate the Document with EntityEntry objects.
    A Document can also contain metadata (e.g. name, author, source).
    '''

    def __init__(self, text="", identifier=None):
        super().__init__()
        self.text = text  # type: str
        self.components = []  # type: List[DocumentComponent]
        self.entities = []  # type: List[EntityEntry]
        self.idenfitier = identifier  # type: int

    def add_component(self, component):
        self.components.append(component)

    def add_entity(self, entity):
        self.entities.append(entity)

    def as_dict(self):
        doc = {}

        # Components
        doc['components'] = list(map(lambda x: x.as_dict(), self.components))
        doc['metadata'] = self.metadata
        doc['entities'] = list(map(lambda x: x.as_dict(), self.entities))

        return doc


class DocumentComponent:
    '''
    A wrapper around the actual document content.
    The `type` field allows you to store structural information (e.g. heading, table).
    '''

    def __init__(self, type, text):
        self.type = type  # type: str
        self.text = text  # type: str

    def as_dict(self):
        return {'type': self.type, 'text': self.text}


class EntityEntry(HasMetadata, HasText):
    '''
    Each entity has a name (e.g. Apple) and a list of AttributeEntry objects.
    An EntityEntry can also contain metadata (e.g. child entities?)
    '''

    def __init__(self, entity):
        HasMetadata.__init__(self)
        HasText.__init__(self, entity)
        self.attributes = []  # type: List[AttributeEntry]

    def add_attribute(self, attribute):
        '''
        :param attribute: AttributeEntry
        :return: void
        '''
        self.attributes.append(attribute)

    def __repr__(self):
        return self.text
        # return '("{}", [{}])'.format(self.text, ", ".join(map(str, self.attributes)))

    def as_dict(self):
        entity_dict = {}

        entity_dict['entity'] = self.text
        entity_dict['attributes'] = list(map(lambda x: x.as_dict(), self.attributes))
        return entity_dict


class AttributeEntry(HasMetadata, HasText):
    '''
    Each AttributeEntry must contain the attribute name and a list of ExpressionEntry objects
    '''

    def __init__(self, attribute, expressions=[]):
        HasMetadata.__init__(self)
        HasText.__init__(self, attribute)
        self.expressions = expressions  # type: List[ExpressionEntry]

    def add_expression(self, expression):
        self.expressions.append(expression)

    def __repr__(self):
        return '("{}", [{}])'.format(self.text, ", ".join(map(str, self.expressions)))

    def as_dict(self):
        attribute_dict = {}

        attribute_dict['attribute'] = self.text
        attribute_dict['expressions'] = list(map(lambda x: x.as_dict(), self.expressions))
        return attribute_dict


class ExpressionEntry(HasMetadata, HasText):
    '''
    Each ExpressionEntry must contain the text of the expression and the id of the originating document.
    Sentiment values can be optionally added (depending on the approach).
    '''

    def __init__(self, expression, sentiment=None, document_id=None):
        HasMetadata.__init__(self)
        HasText.__init__(self, expression)
        self.sentiment = sentiment
        self.document_id = document_id

    def __repr__(self):
        return '("{}", {})'.format(self.text, self.sentiment)

    def as_dict(self):
        expression_dict = {}

        expression_dict['expression'] = self.text
        expression_dict['sentiment'] = self.sentiment
        return expression_dict


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
    def preprocess(self, document_string, extension):
        '''
        Given a document (of any kind), adapts it to a Document object.

        :param document_string:
        :param extension
        :rtype: Document
        '''
        pass


class ExtractorService(abc.ABC):
    @abc.abstractmethod
    def extract(self, doc: Document, verbose: bool) -> Document:
        '''
        Extracts the entity/attribute pairs from the Document object.
        Performs sentiment analysis using the embedded service.
        Annotates the Document object with the extractedEntityEntry objects.
        Returns the annotated Document.

        :param doc: Document
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
