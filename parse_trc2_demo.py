import parse_trc2

name = 'data/1.txt'
file = open(name)

parse_trc2.prepare(file)

for _ in range(100):
    line = parse_trc2.next(file, True)

    if line is None:
        break

    print(line)

file.close()
