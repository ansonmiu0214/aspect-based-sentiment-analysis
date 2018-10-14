import sentiwordnet_parser

name = 'data/SentiWordNet_3.0.0_20130122.txt'
file = open(name)

dictionary = sentiwordnet_parser.parse(file)

print('good', dictionary['good'])
print('bad', dictionary['bad'])

file.close()
