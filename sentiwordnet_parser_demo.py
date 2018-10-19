import sentiwordnet_parser

name = 'data/SentiWordNet_3.0.0_20130122.txt'
file = open(name)

dictionary = sentiwordnet_parser.parse(file)

for word in ['good', 'bad']:
    for type in ['a', 'n', 'v', 'r']:
        print(word, type, sentiwordnet_parser.get_polarity(dictionary, word, type))

file.close()
