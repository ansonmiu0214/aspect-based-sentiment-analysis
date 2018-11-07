import random
import thinc.extra.datasets
import re


class Loader:
  def __init__(self, limit=0, split=0.8):
    self.limit = limit
    self.split = split

  def load_data_default(self):
    train_data, _ = thinc.extra.datasets.imdb()
    random.shuffle(train_data)
    train_data = train_data[-self.limit:]
    print(train_data)
    texts, labels = zip(*train_data)
    cats = [{'POSITIVE': bool(y)} for y in labels]
    split = int(len(train_data) * self.split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

  def load_data_reviews(self):
    # Load file from yelp dataset
    filename = '../data/data_labelled.txt'
    file = open(filename)
    # create training data
    train_data = []
    # format data
    for line in file:
      tokens = line.split()
      text, label = " ".join(tokens[:-1]), int(tokens[-1])
      train_data.append((text, label))
    random.shuffle(train_data)
    train_data = train_data[-self.limit:]
    texts, labels = zip(*train_data)
    cats = [{'POSITIVE': bool(y)} for y in labels]
    split = int(len(train_data) * self.split)
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])

  def load_data_sentiWord(self):
    name = '../data/SentiWordNet_3.0.0_20130122.txt'
    file = open(name)

    REG = '^([anrv])\t\d+\t([\d\.]+)\t([\d\.]+)\t((?:.+#\d+ )*.+#\d+)\t'
    dict = {}

    lines = file.readlines()
    random.shuffle(lines)

    for i in range(self.limit):
      line = lines[i]

      if line == '':
        break

      if line[0] == '#' or line.strip()[0] == '#':
        continue

      res = re.search(REG, line)

      if res is None:
        raise Exception('Invalid line: ' + line)
      else:
        pos_score = float(res.group(2))
        neg_score = float(res.group(3))
        words_with_ranks = res.group(4).split(' ')
        final_score = pos_score - neg_score

        for word_with_rank in words_with_ranks:
          word, rank = word_with_rank.rsplit('#', 1)
          dict[word] = final_score

    return list(dict.keys()), list(dict.values())
