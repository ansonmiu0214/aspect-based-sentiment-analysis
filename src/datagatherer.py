import csv
import sys
from pprint import pprint

from aggregator_service.average_aggregator import AverageAggregator
from data_source.VolatileSource import VolatileSource
from data_source.database_source import DatabaseSource
from extractor_service.spacy_extractor import SpacyExtractor
from models import ExtractorService, SentimentService, PreprocessorService, QueryParser, AggregatorService, \
    DataSourceService
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader
from main import ABSA

def extract_all_tuples(doc):
    all_tuples = list()
    for ent in doc.entities:
        for attr in ent.attributes:
            for exp in attr.expressions:
                all_tuples.append(
                        {
                            'entity': ent.name,
                            'attribute': attr.attribute,
                            'expression': exp
                        })
    return all_tuples

def label(t):
    pass

def label_all_tuples(tuples):
    return map(label, tuples)

def main(sourcefile):
    sentiment_service = Vader()
    absa = ABSA(preprocessor=TextPreprocessor(),
                extractor=SpacyExtractor(sentiment_service),
                sentiment=sentiment_service,
                datasource=VolatileSource(),
                query_parser=SimpleParser(),
                aggregator=AverageAggregator())

    doc = None
    with open(sourcefile) as file:
        doc = absa.load_document(file)

    print(extract_all_tuples(doc))


    with open('training.csv', 'w', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

if __name__ == '__main__':
    print(sys.argv[1])
    main(sys.argv[1])
