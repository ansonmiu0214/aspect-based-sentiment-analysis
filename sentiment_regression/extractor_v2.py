import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def main(text):
    SKIP_ENTITY_LABELS = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    MODEL = 'en_core_web_sm'

    paragraphs = text.split('\n\n')

    nlp = spacy.load(MODEL)
    entities = {}

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph == '':
            continue

        doc = nlp(paragraph)
        para_polar = 0

        for sentence in doc.sents:
            para_polar += analyser.polarity_scores(sentence.text)['compound']

        # print('para polar:', para_polar)

        if para_polar != 0:
            for entity in doc.ents:
                if entity.label_ not in SKIP_ENTITY_LABELS and entity.lemma_ != '':
                    if entity.lemma_ in entities:
                        entities[entity.lemma_]['count'] += 1
                        entities[entity.lemma_]['sentiment'] += para_polar
                    else:
                        entities[entity.lemma_] = {'count': 1, 'sentiment': para_polar}

    res = list(map(lambda x: {'entity': x[0], 'count': x[1]['count'], 'sentiment': x[1]['sentiment'], },
                   sorted(entities.items(), key=lambda x: x[1]['count'], reverse=True)))

    print(res)


# From Reuters.
text = """\
Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on Thursday, with its departing chief executive saying his recovery plan was working.

Gavin Patterson, who is being replaced as CEO by Worldpay’s Philip Jansen in February, said BT was improving customer service, accelerating the roll-out of full-fibre networks and transforming its operating model.

Shares in the British leader in both broadband and mobile rose by more than 10 percent after it nudged its guidance for the full year higher and first-half earnings rose 2 percent.

“Despite increasingly competitive fixed, mobile and networking markets and continued declines in legacy products there is no change in our overall outlook for the full year,” Patterson said, adding that based on current trading the company expected earnings to be in the upper half of its range.

Citi analysts, who have a “neutral” rating on BT shares, highlighted “steady improvements in the underlying trends”.

Patterson, who has run BT for more than five years, announced a shake-up in May to address a damaging accounting scandal and a poor customer service record.

However, a lukewarm reaction to the strategy, which involved 13,000 job cuts, led chairman Jan du Plessis to decide a leadership change was needed.

Patterson said the plan was working and he intended to maintain momentum as he prepared his departure.

“We were confident of our strategy when we set it out in May and the strategy had a three-to-five year horizon,” he said.

BT posted adjusted half-year core earnings of 3.68 billion pounds ($4.74 billion) and said it expected earnings for the year to be at the upper end of its 7.3-7.4 billion pound range.

Adjusted revenue slipped 1 percent to 11.62 billion pounds as regulated price reductions in its broadband network, which serves other operators as well as BT, and declines in its enterprise businesses offset growth in consumer.

BT’s shares rose to 266 pence, their highest since January, but are well off a high of 5 pounds during Patterson’s tenure and trade on only around a nine times forward earnings multiple.
"""

main(text)
