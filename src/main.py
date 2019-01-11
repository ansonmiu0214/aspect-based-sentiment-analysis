from aggregator_service.average_aggregator import AverageAggregator
from data_source.VolatileSource import VolatileSource
from data_source.database_source import DatabaseSource
from extractor_service.spacy_extractor import SpacyExtractor
from models import ExtractorService, SentimentService, PreprocessorService, QueryParser, AggregatorService, \
    DataSourceService, Query
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader


class ABSA:
    def __init__(self, preprocessor, extractor, sentiment, datasource, query_parser, aggregator):
        self.preprocessor_service = preprocessor  # type: PreprocessorService
        self.extractor_service = extractor        # type: ExtractorService
        self.sentiment_service = sentiment        # type: SentimentService
        self.data_source = datasource             # type: DataSourceService
        self.query_parser = query_parser          # type: QueryParser
        self.aggregator_service = aggregator      # type: AggregatorService

    def load_document(self, document_string, extension="txt", verbose=True):
        '''
        Load and process a document of any form, returning the stored document id.

        :param document_string: str
        :param extension: str
        :param verbose: bool
        :rtype: int
        '''

        doc = self.preprocessor_service.preprocess(document_string, extension)
        if verbose:
            print("Preprocessing complete.")

        doc = self.extractor_service.extract(doc, verbose=verbose)
        if verbose:
            print("Extraction complete.")
            print("Entities found: {}".format(", ".join(map(lambda ent: ent.text, doc.entities))))

        doc_id = self.data_source.process_document(doc)
        if verbose:
            print("Document processed into data source.")

        return doc_id

    def process_query(self, entity, attribute, verbose=False):
        '''
        Process the user query and return the aggregated sentiment and related entries.

        :param query: str
        :rtype: (float, List[AttributeEntry])
        '''

        query = Query(entity, attribute)
        if verbose:
            print("Query parsed.")

        relevant_entries = self.data_source.lookup(query)
        count = len(relevant_entries)
        if verbose:
            print("{} relevant entr{} found.".format(count, "y" if count == 1 else "ies"))

        if count == 0:
            return None, []

        aggregateData = [{'sentiment': expr.sentiment, 'is_header': expr.is_header}
                         for entry in relevant_entries for expr in entry.expressions]
        score = self.aggregator_service.aggregate_sentiment(aggregateData)
        if verbose:
            print("Sentiment scores aggregated.")

        return score, relevant_entries
