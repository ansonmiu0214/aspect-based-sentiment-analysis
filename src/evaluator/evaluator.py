import json

from data_source.database_source import DatabaseSource
from metric import document_error
from extractor_service.spacy_extractor import SpacyExtractor
from models import *
from preprocessor_service.text_preprocessor import TextPreprocessor
from sentiment_service.vader import Vader


def json_to_dict(entries):
    entities = {}

    for entry in entries:
        entity = entry['entity']
        attribute = entry['attribute']
        expression = entry['expression']
        sentiment = entry['sentiment']

        if entity not in entities:
            entities[entity] = {}

        if attribute not in entities[entity]:
            entities[entity][attribute] = []

        entities[entity][attribute].append(ExpressionEntry(expression, sentiment))

    return entities


def json_to_entities(json_string: str) -> List[EntityEntry]:
    entries = json.loads(json_string)
    entities = json_to_dict(entries)

    entity_entries = []
    for entity in entities:
        entity_entry = EntityEntry(entity)

        attributes = entities[entity]
        for attribute in attributes:
            expr_entries = attributes[attribute]
            attr_entry = AttributeEntry(attribute, expr_entries)
            entity_entry.add_attribute(attr_entry)
        entity_entries.append(entity_entry)
    return entity_entries


def update_tags_from_json(document: Document, json_string: str) -> Document:
    '''
    Given a Document object that has already been preprocessed with the DocumentComponents
    and a well-formatted JSON string of the ground truth tags, returns the annotated Document.
    '''

    entities = json_to_entities(json_string)
    for entity in entities:
        document.add_entity(entity)
    return document


class Evaluator:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.sentiment_service = Vader()
        self.extractor = SpacyExtractor(self.sentiment_service)
        self.db = DatabaseSource(is_production=False)
        pass

    def load_test_document(self, doc_string: str, ground_truth_json: str):
        # TODO generalise the preprocess function to be applied on strings only
        document = self.preprocessor.preprocess_xml_text(doc_string)
        document = update_tags_from_json(document, ground_truth_json)

        self.db.process_document(document)

    def reset_all_test_documents(self):
        self.db.reset()

    def run_evaluator(self):
        # Get all documents
        all_docs = self.db.list_all_documents()

        doc_count = len(all_docs)
        if doc_count == 0:
            return None

        total_score = 0

        for id in all_docs:
            doc = self.db.retrieve_document(id)

            ground_truth = list(doc.entities)

            doc.entities = []
            doc = self.extractor.extract(doc)

            score = document_error(doc.entities, ground_truth)
            total_score += score

        avg_score = total_score / doc_count
        return avg_score


# if __name__ == '__main__':

xml_text = """<?xml version="1.0" encoding="iso-8859-1" ?>
<newsitem itemid="2286" id="root" date="1996-08-20" xml:lang="en">
<title>MEXICO: Recovery excitement brings Mexican markets to life.</title>
<headline>Recovery excitement brings Mexican markets to life.</headline>
<byline>Henry Tricks</byline>
<dateline>MEXICO CITY</dateline>
<text>
<p>Emerging evidence that Mexico's economy was back on the recovery track sent Mexican markets into a buzz of excitement Tuesday, with stocks closing at record highs and interest rates at 19-month lows.</p>
<p>&quot;Mexico has been trying to stage a recovery since the beginning of this year and it's always been getting ahead of itself in terms of fundamentals,&quot; said Matthew Hickman of Lehman Brothers in New York.</p>
<p>&quot;Now we're at the point where the fundamentals are with us. The history is now falling out of view.&quot;</p>
<p>That history is one etched into the minds of all investors in Mexico: an economy in crisis since December 1994, a free-falling peso and stubbornly high interest rates.</p>
<p>This week, however, second-quarter gross domestic product was reported up 7.2 percent, much stronger than most analysts had expected. Interest rates on governent Treasury bills, or Cetes, in the secondary market fell on Tuesday to 23.90 percent, their lowest level since Jan. 25, 1995.</p>
<p>The stock market's main price index rallied 77.12 points, or 2.32 percent, to a record 3,401.79 points, with volume at a frenzied 159.89 million shares.</p>
<p>Confounding all expectations has been the strength of the peso, which ended higher in its longer-term contracts on Tuesday despite the secondary Cetes drop and expectations of lower benchmark rates in Tuesday's weekly auction.</p>
<p>With U.S. long-term interest rates expected to remain steady after the Federal Reserve refrained from raising short-term rates on Tuesday, the attraction of Mexico, analysts say, is that it offers robust returns for foreigners and growing confidence that they will not fall victim to a crumbling peso.</p>
<p>&quot;The focus is back on Mexican fundamentals,&quot; said Lars Schonander, head of researcher at Santander in Mexico City. &quot;You have a continuing decline in inflation, a stronger-than-expected GDP growth figure and the lack of any upward move in U.S. rates.&quot;</p>
<p>Other factors were also at play, said Felix Boni, head of research at James Capel in Mexico City, such as positive technicals and economic uncertainty in Argentina, which has put it and neighbouring Brazil's markets at risk.</p>
<p>&quot;There's a movement out of South American markets into Mexico,&quot; he said. But Boni was also wary of what he said could be &quot;a lot of hype.&quot;</p>
<p>The economic recovery was still export-led, and evidence was patchy that the domestic consumer was back with a vengeance. Also, corporate earnings need to grow strongly to justify the run-up in the stock market, he said.</p>
</text>
<copyright>(c) Reuters Limited 1996</copyright>
<metadata>
<codes class="bip:countries:1.0">
  <code code="MEX">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
</codes>
<codes class="bip:topics:1.0">
  <code code="E11">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
  <code code="ECAT">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
  <code code="M11">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
  <code code="M12">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
  <code code="MCAT">
    <editdetail attribution="Reuters BIP Coding Group" action="confirmed" date="1996-08-20"/>
  </code>
</codes>
<dc element="dc.publisher" value="Reuters Holdings Plc"/>
<dc element="dc.date.published" value="1996-08-20"/>
<dc element="dc.source" value="Reuters"/>
<dc element="dc.creator.location" value="MEXICO CITY"/>
<dc element="dc.creator.location.country.name" value="MEXICO"/>
<dc element="dc.source" value="Reuters"/>
</metadata>
</newsitem>
"""

# json_string = """[{"entity":"Mexico","attribute":"economy","expression":"Emerging evidence that Mexico 's economy was back on the recovery track sent Mexican markets into a buzz of excitement Tuesday , with stocks closing at record highs and interest rates at 19-month lows","sentiment":0.6}]
# """

json_string = """[{"entity":"Mexico","attribute":"economy","expression":"Emerging evidence that Mexico's economy was back on the recovery track sent Mexican markets into a buzz of excitement Tuesday, with stocks closing at record highs and interest rates at 19-month lows.","sentiment":0.9}, {"entity":"Mexico","attribute":"gross domestic product","expression":"second-quarter gross domestic product was reported up 7.2 percent, much stronger than most  analysts had expected","sentiment":0.8}, {"entity":"Mexico","attribute":"economy","expression":"an economy in crisis  since December 1994, a free-falling peso and stubbornly high interest rates.","sentiment":-0.5}]"""

evaluator = Evaluator()
# evaluator.reset_all_test_documents()
# evaluator.load_test_document(doc_string=xml_text, ground_truth_json=json_string)
print(evaluator.run_evaluator())

# entities = json_to_entities(json_string)
# for entity in entities:
#     print(entity)
#
#     for attr in entity.attributes:
#         print(attr)
#         print(attr.expressions)
