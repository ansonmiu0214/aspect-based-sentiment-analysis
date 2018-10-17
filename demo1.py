import extractor
import sentiwordnet_parser
import trc2_parser

LIMIT = 1000

trc2_file = open('data/headlines.txt')
sentiwordnet_file = open('data/SentiWordNet_3.0.0_20130122.txt')

trc2_parser.prepare(trc2_file)
nlp = extractor.load_model()
senti_dict = sentiwordnet_parser.parse(sentiwordnet_file)

count = 0
index = 0

for index in range(LIMIT):
    (date, headline) = trc2_parser.next(trc2_file, False)

    if headline is None:
        break

    extract = extractor.extract(nlp, headline)

    for (entity, attributes, negate, word_with_types) in extract:
        entity_polarity = 0
        polar_words = []

        for (word, type) in word_with_types:
            word_polarity = sentiwordnet_parser.get_polarity(senti_dict, word, type)
            if word_polarity != 0:
                entity_polarity += word_polarity
                polar_words.append((word, type))

        if negate:
            entity_polarity *= -1

        if entity_polarity != 0:
            print(date, entity, attributes, entity_polarity, polar_words, negate)
            count += 1

trc2_file.close()

print(str(count) + ' of ' + str(index + 1) + ' headlines have sentiment.')
