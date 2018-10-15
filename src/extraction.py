import spacy


def extract_phrase(eas):
    entity, _, sentiment = eas
    doc = entity.doc
    entity_index = entity.i
    sentiment_index = sentiment.i
    phrase = ""
    if entity_index < sentiment_index:
        current = entity_index
        while current <= sentiment_index:
            phrase += doc[current].text
            current += 1
    else:
        current = sentiment_index
        while current <= entity_index:
            phrase += doc[current].text
            current += 1
    return phrase

