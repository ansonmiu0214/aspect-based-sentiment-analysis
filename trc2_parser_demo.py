import trc2_parser

name = 'data/trc2.csv'
file = open(name)

trc2_parser.prepare(file)

for _ in range(100):
    line = trc2_parser.next(file, True)

    if line is None:
        break

    print(line)

file.close()
