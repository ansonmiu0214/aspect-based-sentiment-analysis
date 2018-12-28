from models import EntityEntry, AttributeEntry
from preprocessor_service.text_preprocessor import TextPreprocessor


def annotate_document(doc, tags):
    for ent in tags:
        entity = EntityEntry(ent)
        for attr in tags[ent]:
            exprs = []
            sents = 0
            for expr, sent in tags[ent][attr]:
                exprs.append(expr)
                sents += sent
            attribute = AttributeEntry(attr, exprs, sents)
            entity.add_attribute(attribute)
        doc.add_entity(entity)


def preprocess_tags(tags):
    processed_tags = {}

    for ent, attr, expr, sent in tags:
        if ent not in processed_tags:
            processed_tags[ent] = dict()

        if attr not in processed_tags[ent]:
            processed_tags[ent][attr] = []

        processed_tags[ent][attr].append((expr, sent))

    return processed_tags


def get_original_doc():
    preprocessor = TextPreprocessor()

    file = open('2286newsML.xml', 'r')
    file.filename = '2286newsML.xml'
    doc = preprocessor.preprocess(file)
    return doc


def get_doc():
    preprocessor = TextPreprocessor()

    file = open('2286newsML.xml', 'r')
    file.filename = '2286newsML.xml'
    doc = preprocessor.preprocess(file)

    tags = [
        (
            'Mexico',
            'economy',
            '''Emerging evidence that Mexico's economy was back on the recovery track 
            sent Mexican markets into a buzz of excitement Tuesday, with stocks closing 
            at record highs and interest rates at 19-month lows.''',
            0.9
        ),
        (
            'Mexico',
            'gross domestic product',
            '''
            second-quarter gross domestic product was reported up 7.2 percent, 
            much stronger than most analysts had expected
            ''',
            0.8
        ),
        (
            'Mexico',
            'economy',
            '''
            an economy in crisis since December 1994, a free-falling peso and stubbornly high interest rates.
            ''',
            -0.5
        )
    ]

    tags = preprocess_tags(tags)
    annotate_document(doc, tags)

    return doc


if __name__ == '__main__':
    get_doc()
