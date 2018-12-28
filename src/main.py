from pprint import pprint
import sys

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
        self.extractor_service = extractor  # type: ExtractorService
        self.sentiment_service = sentiment  # type: SentimentService
        self.data_source = datasource  # type: DataSourceService
        self.query_parser = query_parser  # type: QueryParser
        self.aggregator_service = aggregator  # type: AggregatorService

    def load_document(self, input_document, verbose=False):
        '''
        Load and process a document of any form.

        :param input_document:
        :return: void
        '''
        doc = self.preprocessor_service.preprocess(input_document)
        if verbose:
            print("Preprocessing complete.")

        doc = self.extractor_service.extract(doc, verbose=True)
        if verbose:
            print("Extraction complete.")
            print("Entities found: {}".format(", ".join(map(lambda ent: ent.text, doc.entities))))

        self.data_source.process_document(doc)
        if verbose:
            print("Document processed into data source.")

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

        sentiments = [expr.sentiment for entry in relevant_entries for expr in entry.expressions]
        score = self.aggregator_service.aggregate_sentiment(sentiments)
        if verbose:
            print("Sentiment scores aggregated.")

        return score, relevant_entries


if __name__ == '__main__':
    sentiment_service = Vader()
    # sentiment_service = BagOfWords()

    absa = ABSA(preprocessor=TextPreprocessor(),
                extractor=SpacyExtractor(sentiment_service),
                sentiment=sentiment_service,
                datasource=VolatileSource(),
                query_parser=SimpleParser(),
                aggregator=AverageAggregator())

    text = """\ Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on 
    Thursday, with its departing chief executive saying his recovery plan was working. 

    Gavin Patterson, who is being replaced as CEO by Worldpay's Philip Jansen in February, said BT was improving 
    customer service, accelerating the roll-out of full-fibre networks and transforming its operating model. 

    Shares in the British leader in both broadband and mobile rose by more than 10 percent after it nudged its 
    guidance for the full year higher and first-half earnings rose 2 percent. 

    "Despite increasingly competitive fixed, mobile and networking markets and continued declines in legacy products 
    there is no change in our overall outlook for the full year," Patterson said, adding that based on current 
    trading the company expected earnings to be in the upper half of its range. 

    Citi analysts, who have a "neutral" rating on BT shares, highlighted "steady improvements in the underlying trends".

    Patterson, who has run BT for more than five years, announced a shake-up in May to address a damaging accounting 
    scandal and a poor customer service record. 

    However, a lukewarm reaction to the strategy, which involved 13,000 job cuts, led chairman Jan du Plessis to 
    decide a leadership change was needed. 

    Patterson said the plan was working and he intended to maintain momentum as he prepared his departure.

    "We were confident of our strategy when we set it out in May and the strategy had a three-to-five year horizon,
    " he said. 

    BT posted adjusted half-year core earnings of 3.68 billion pounds ($4.74 billion) and said it expected earnings 
    for the year to be at the upper end of its 7.3-7.4 billion pound range. 

    Adjusted revenue slipped 1 percent to 11.62 billion pounds as regulated price reductions in its broadband 
    network, which serves other operators as well as BT, and declines in its enterprise businesses offset growth in 
    consumer. 

    BT's shares rose to 266 pence, their highest since January, but are well off a high of 5 pounds during 
    Patterson's tenure and trade on only around a nine times forward earnings multiple. """

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as file:
            absa.load_document(file, verbose=True)
    else:
        absa.load_document(text, verbose=True)

    while True:
        print('============')
        print('Enter entity to query: ', end='')
        entity = input().strip()
        if entity == '':
            break
        print('Enter attribute to query (can leave blank): ', end='')
        attribute = input().strip()

        score, entry = absa.process_query(entity, attribute, verbose=True)
        print(score)
        pprint(entry)
