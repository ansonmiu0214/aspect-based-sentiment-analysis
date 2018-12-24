import csv
import sys
import string
import spacy
import os
import pathlib
from fnmatch import fnmatch
from pprint import pprint

from aggregator_service.average_aggregator import AverageAggregator
from extractor_service.spacy_extractor import SpacyExtractor
from models import ExtractorService, SentimentService, PreprocessorService, QueryParser, AggregatorService, \
    DataSourceService
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader
from main import ABSA

nlp = spacy.load('en_core_web_sm')
PATTERN = '*.xml'

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
                        }
                )
    return all_tuples


def find_sublist(s, l):
    start = -1
    matched = 0
    for (i, word) in enumerate(l):
        if matched == len(s):
            break

        if s[matched].lower() == word.lower():
            matched += 1
            if start == -1:
                start = i
        else:
            matched = 0
            start = -1

    if matched == len(s):
        return start
    return -1


def format_for_matching(s):
    doc = nlp(s)
    sent = list(doc.sents)[0]
    return list(map(lambda t: t.text, sent))


def adjust_heads(heads, deps):
    start = 0
    end = start
    while end < len(heads):
        if deps[end] == '-':
            end += 1
        else:
            for i in range(start, end):
                heads[i] = i + 1
            start = end + 1
            end = start

    if start != end:
        for i in range(start, end):
            heads[i] = i - 1


def label(t):
    ent = t['entity'].lower().split()
    attr = t['attribute'].lower().split()
    exp = t['expression']
    sep = format_for_matching(exp)
    length = len(sep)
    heads = [0] * length
    deps = ['-'] * length

    ent_start = find_sublist(ent, sep)

    # Ignore coreferencing instances
    if ent_start == -1:
        return None

    heads[ent_start] = ent_start
    deps[ent_start] = 'ENTITY'
    for i in range(ent_start + 1, ent_start + len(ent)):
        heads[i] = i - 1
        deps[i] = 'ENTITY_ADD'

    attr_start = find_sublist(attr, sep)
    # Allow possibility of no attribute
    if attr_start != -1:
        heads[attr_start] = ent_start
        deps[attr_start] = 'ATTRIBUTE'
        for i in range(attr_start + 1, attr_start + len(attr)):
            heads[i] = i - 1
            deps[i] = 'ATTRIBUTE_ADD'

    adjust_heads(heads, deps)
    return {'expression': exp, 'words': sep, 'heads': heads, 'deps' : deps}


def label_all_tuples(tuples):
    return map(label, tuples)


def extract_data(absa, writer, filename):
    with open(filename) as file:
        doc = absa.load_document(file)
        all_tuples = extract_all_tuples(doc)
        labelled = label_all_tuples(all_tuples)

        # Remove coreferencing artifacts
        labelled = filter(lambda x: x is not None, labelled)
        for data in labelled:
            writer.writerow(data)


def main(directory):
    sentiment_service = Vader()
    absa = ABSA(preprocessor=TextPreprocessor(),
                extractor=SpacyExtractor(sentiment_service),
                sentiment=sentiment_service,
                datasource=None,
                query_parser=SimpleParser(),
                aggregator=AverageAggregator())

    i = 0
    with open('training.csv', 'w', newline='') as csvfile:
        fieldnames = ['expression', 'words', 'heads', 'deps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for path, subdirs, files in os.walk(directory):
            for name in files:
                if fnmatch(name, PATTERN):
                    extract_data(absa, writer, pathlib.PurePath(path, name))
                    i += 1
                    print("{} document processed.".format(i))
                    if i == 100:
                        return


if __name__ == '__main__':
    main(sys.argv[1])
