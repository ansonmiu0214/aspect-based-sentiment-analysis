# Functions to read trc2 data sets (trc2.csv or headlines.txt by default).

import re


def prepare(file):
    # Seek past useless first line.
    file.readline()


# Returns (date, headline, body) or (date, headline).
def next(file, has_body):
    line = file.readline()
    if line == '':
        return None
    else:
        if has_body:
            reg = '^([\d\-/ :]+),"(.+)"(?!"),"(?!")(.+)"\s*$'
        else:
            reg = '^([\d\-/ :]+),"(.+)"(?!")\s*$'
        res = re.search(reg, line)
        if res is None:
            raise Exception('Invalid line: ' + line)
        elif has_body:
            return res.group(1), res.group(2).replace('""', '"'), res.group(3).replace('""', '"')
        else:
            return res.group(1), res.group(2).replace('""', '"')
