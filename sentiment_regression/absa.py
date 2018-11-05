from argparse import ArgumentParser
import extractor
import bag_of_words

default_text = "The iPhone has a great camera but a poor screen. The MacBook has excellent battery, just like the " \
               "iPhone. The iPhone and MacBook also have terrible prices. "
default_entity = "iPhone"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-d', '--document')
    parser.add_argument('-t', '--text')
    parser.add_argument('-e', '--entity', default=None)
    parser.add_argument('-f', '--training', required=True, help="Directory to training sentences")

    args = parser.parse_args()

    entity = args.entity
    if not args.text:
        args.text = default_text
        entity = default_entity

    data = ''
    if args.document:
        with open(args.document, 'r') as f:
            data = f.read().replace('\n', '')
    else:
        data = args.text

    # Extractor pipeline.
    eas = extractor.main(data, entity)
    print("Relevant aspects: {}".format(eas))

    # Sentiment analyser.
    # TODO:refine this
    model = bag_of_words.BOWModel()
    model.train_model(args.training)

    # TODO:Move this to evaluation model
    aggregation = []

    for entry in eas:
        entity, attribute, sentiment = entry
        [score] = model.predict(sentiment)
        aggregation.append((entry, score))

    print(aggregation)
