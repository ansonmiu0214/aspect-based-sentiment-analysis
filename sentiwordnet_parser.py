# Parser for SentiWordNet data set from https://sentiwordnet.isti.cnr.it ('SentiWordNet_3.0.0_20130122.txt' by default).
# Based on Java demo at https://sentiwordnet.isti.cnr.it/code/SentiWordNetDemoCode.java

import re


# Return a mapping of words to sentiment polarity ([-1, 1]).
def parse(file):
    REG = '^[anrv]\t\d+\t([\d\.]+)\t([\d\.]+)\t((?:.+#\d+ )*.+#\d+)\t'
    tmp_dict = {}

    while True:
        line = file.readline()

        if line == '':
            break

        if line[0] == '#' or line.strip()[0] == '#':
            continue

        res = re.search(REG, line)

        if res is None:
            raise Exception('Invalid line: ' + line)
        else:
            pos_score = float(res.group(1))
            neg_score = float(res.group(2))
            words_with_ranks = res.group(3).split(' ')
            final_score = pos_score - neg_score

            for word_with_rank in words_with_ranks:
                word, rank = word_with_rank.rsplit('#', 1)
                rank = int(rank)
                if word in tmp_dict:
                    tmp_dict[word][rank] = final_score
                else:
                    tmp_dict[word] = {rank: final_score}

    dict = {}

    # Merge ranks and scores using weight-average.
    for word, ranks_with_scores in tmp_dict.items():
        sum_score = 0
        sum_ranks = 0

        for rank, score in ranks_with_scores.items():
            sum_score += score / rank
            sum_ranks += 1 / rank

        dict[word] = sum_score / sum_ranks

    return dict
