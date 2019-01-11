import pprint
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

ENT_WITH_ATTR_BLACKLIST = ['LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
ENT_TO_EXTRACT_BLACKLIST = ['PERSON', 'LANGUAGE', 'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
ATTR_BLACKLIST = ['high', 'low', 'max', 'maximum', 'min', 'minimum', 'growth', 'trend', 'improvement']
MODEL = 'en_core_web_sm'  # en_core_web_sm


def is_valid_attribute_token(token):
    if token.text == 'out':
        print(token, token.pos_, token.sent)

    # Skip if part of entity (e.g. 'pound' is MONEY).
    if token.ent_iob_ != 'O':
        return False

    # Skip if not noun.
    if token.pos_ != 'NOUN':
        return False

    # Skip nouns like 'who'.
    if token.tag_ == 'WP':
        return False

    # Skip quantifier modifier (e.g. 'times' in '5 times').
    if token.dep_ == 'quantmod':
        return False

    return True


def retrieve_attribute(token):
    s = token.lemma_
    cur = token

    while True:
        compound = next(filter(lambda x: x.dep_ == 'compound', cur.children), None)

        if compound is None or not is_valid_attribute_token(compound):
            break
        else:
            cur = compound
            s = compound.lemma_ + ' ' + s

    return s

def main(text):
    nlp = spacy.load(MODEL)
    paragraphs = text.split('\n\n')
    ents_to_extract = {}

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if paragraph == '':
            continue

        doc = nlp(paragraph)

        # Calculate polarity of paragraph.
        para_polar = sum(map(lambda sent: analyser.polarity_scores(sent.text)['compound'], doc.sents))

        if para_polar == 0:
            continue

        para_ents_with_attr = {}

        # Extract entities and add sentiments.
        for ent in filter(lambda x: x.label_ not in ENT_TO_EXTRACT_BLACKLIST and x.lemma_ != '', doc.ents):
            if ent.lemma_ in ents_to_extract:
                ents_to_extract[ent.lemma_]['count'] += 1
                ents_to_extract[ent.lemma_]['sentiment'] += para_polar
            else:
                ents_to_extract[ent.lemma_] = {'count': 1, 'sentiment': para_polar, 'attributes': {}}

        # Map indices to entities.
        for ent in filter(lambda x: x.label_ not in ENT_WITH_ATTR_BLACKLIST and x.lemma_ != '', doc.ents):
            para_ents_with_attr[ent[0].i] = ent

        # Extract attributes and add sentiments.
        cur_entity = None
        cur_sent_polar = None
        for token in doc:
            # Reset current sentence polarity if new sentence.
            is_sent_start = token.sent.start == token.i
            if is_sent_start:
                cur_sent_polar = None

            # Skip if current sentence has 0 polarity.
            if cur_sent_polar == 0:
                continue

            # Set current entity.
            if token.ent_iob_ == 'B' and token.i in para_ents_with_attr:
                cur_entity = para_ents_with_attr[token.i]
                if cur_entity.label_ in ENT_TO_EXTRACT_BLACKLIST:
                    cur_entity = None

            # Skip if no attached entity.
            if cur_entity is None:
                continue

            # Skip if compound (i.e. part of multi-word attribute)
            # Compound token will be gotten together with the base token.
            if token.dep_ == 'compound':
                continue

            # Skip if not valid attribute token.
            if not is_valid_attribute_token(token):
                continue

            # Retrieve attribute.
            attribute = retrieve_attribute(token)

            # Skip if in blacklist.
            if attribute in ATTR_BLACKLIST:
                continue

            if cur_sent_polar is None:
                cur_sent_polar = analyser.polarity_scores(token.sent.text)['compound']

            # Skip if current sentence has 0 polarity.
            if cur_sent_polar == 0:
                continue

            ent_attributes = ents_to_extract[cur_entity.lemma_]['attributes']
            if attribute in ent_attributes:
                ent_attributes[attribute]['count'] += 1
                ent_attributes[attribute]['sentiment'] += cur_sent_polar
            else:
                ent_attributes[attribute] = {'count': 1, 'sentiment': cur_sent_polar}

    # Sort entities by count.
    res = sorted(ents_to_extract.items(), key=lambda x: x[1]['count'], reverse=True)

    pprint.pprint(res)


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


if __name__ == '__main__':
    main(text)
