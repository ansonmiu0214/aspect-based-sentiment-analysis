# import newsdocument
import random

import numpy as np
import spacy

from extractor_service.spacy_extractor import SpacyExtractor
from sentiment_service.vader import Vader

nlp = spacy.load('en_core_web_sm')


def document_error(model_output, ground_truth):
    '''

    :param model_output:
    :param ground_truth:
    :return:
    '''
    loss_score = 0
    sent_mse = 0
    sent_count = 0

    ent_tp = 0
    ent_fp = 0
    ent_fn = 0

    attr_tp = 0
    attr_fp = 0
    attr_fn = 0

    mse = 0

    tp_dict = {}

    matched_ents = set()
    for ent in model_output:
        matched_entity = token_match(ent, ground_truth, "E")
        if matched_entity is not None:
            if matched_entity.text not in tp_dict:
                tp_dict[matched_entity.text] = {}
                ent_tp += 1

            # if matched_entity not in matched_ents:
            #     matched_ents.add(matched_entity)
            #     ent_tp += 1
            curr_tp = 0
            curr_fp = 0

            matched_attrs = set()
            for attr in ent.attributes:
                matched_attribute = token_match(attr, matched_entity.attributes, "A")

                if matched_attribute is not None:

                    sent_count += 1
                    if matched_attribute.text not in tp_dict[matched_entity.text]:
                        tp_dict[matched_entity.text][matched_attribute.text] = True
                        curr_tp += 1

                        pred_score = 0
                        ground_score = 0
                        ground_num = 0
                        pred_num = 0

                        for expr in attr.expressions:
                            ground_score += expr.sentiment
                            ground_num += 1

                        for expr in matched_attribute.expressions:
                            pred_score += expr.sentiment
                            pred_num += 1

                        sent_mse += ((ground_score/ground_num) - (pred_score/pred_num))**2







                        # if matched_attribute not in matched_attrs:
                        #     matched_attrs.add(matched_attribute)
                        #     curr_tp += 1

                        # for expr in attr.expressions:
                        #     diff = find_similar_phrase(expr, attr.expressions)
                        #     loss_score += diff
                else:
                    print("ENT %s attr fp: model= %s" % (ent.text, attr.text))
                    curr_fp += 1

            attr_tp += curr_tp
            attr_fp += curr_fp
            attr_fn += len(matched_entity.attributes) - curr_tp
        else:
            ent_fp += 1

    sent_mse = (sent_mse / sent_count)

    print("GT %s" % ground_truth)

    ent_fn += len(ground_truth) - ent_tp

    ent_precision = ent_recall = ent_f1 = 0


    if ent_tp == ent_fp == ent_fn == 0:
        ent_precision = ent_recall = ent_f1 = 1
    elif ent_tp == 0:
        ent_precision = ent_recall = ent_f1 = 0
    else:
        ent_precision = ent_tp / (ent_tp + ent_fp)
        ent_recall = ent_tp / (ent_tp + ent_fn)
        ent_f1 = 2 * (ent_precision * ent_recall) / (ent_precision + ent_recall)

    attr_precision = attr_recall = attr_f1 = 0
    if attr_tp == attr_fp == attr_fn == 0:
        attr_precision = attr_recall = attr_f1 = 1
    elif attr_tp == 0:
        attr_precision = attr_recall = attr_f1 = 0
    else:
        attr_precision = attr_tp / (attr_tp + attr_fp)
        attr_recall = attr_tp / (attr_tp + attr_fn)

        attr_f1 = 2 * (attr_precision * attr_recall) / (attr_precision + attr_recall)

    loss_score = ent_f1 + attr_f1

    print("Ent precision = %s" % ent_precision)
    print("Ent recall = %s" % ent_recall)
    print("Ent tp = %s" % ent_tp)
    print("Ent fp = %s" % ent_fp)
    print("Ent fn = %s" % ent_fn)
    print("Attr precision = %s" % attr_precision)
    print("Attr recall = %s" % attr_recall)
    print("Attr tp = %s" % attr_tp)
    print("Attr fp = %s" % attr_fp)
    print("Attr fn = %s" % attr_fn)
    print("***")

    return {'score': abs(loss_score),
            'ent_f1': ent_f1,
            'attr_f1': attr_f1,
            'ent_precision': ent_precision,
            'ent_recall': ent_recall,
            'mse': mse,
            'tp': tp_dict
            }


def token_match(input, target_set, type):
    input_text = ""
    original_text = ""

    input_text = input.text

    for token in target_set:
        original_text = token.text
        if input_text.lower() in original_text.lower() or original_text.lower() in input_text.lower():
            return token
    return None


def calculate_error(attr1, attr2):
    if attr1 is None:
        return 2
    else:
        return abs(attr1.sentiment - attr2.sentiment)


def find_similar_phrase(phrase, phrases):
    word_set1 = phrase.text.split(" ")
    word_set1 = sorted(word_set1)

    # print("The original phrase is %s" % phrase)


    idx = 0
    while word_set1[idx] == "" or word_set1[idx] == '\n':
        idx += 1
    word_set1 = word_set1[idx:]
    v1 = nlp(word_set1[0])[0].vector
    for w in word_set1[1:]:
        if w.strip() != '':
            v1 = np.add(v1, nlp(w)[0].vector)

    max_val = -100000000
    min_phrase = ""

    for p in phrases:
        word_set2 = p.text.split(' ')
        word_set2 = sorted(word_set2)
        idx = 0
        while word_set2[idx] == "" or word_set2[idx] == '\n':
            idx += 1
        word_set2 = word_set2[idx:]
        v2 = nlp(word_set1[0])[0].vector

        for w in word_set2[1:]:

            if w.strip() != '':
                v2 = np.add(v2, nlp(w)[0].vector)

        max_length = max(len(v1), len(v2))

        if len(v1) > len(v2):
            for x in range(max_length):
                np.add(v2, 0)
        else:
            for x in range(max_length):
                np.add(v1, 0)

        diff = np.dot(v1, v2) / ((np.linalg.norm(v1)) * np.linalg.norm(v2))

        # print("The current phrase is %s" % p)
        # print("The error of the current phrase is %f" % diff)

        if diff > max_val:
            max_val = diff
            min_phrase = p

    # print("The min val is %f" % min_val)
    # print("The min phrase is %s" % min_phrase)

    return abs(max_val - 1)


def find_most_similar(target, candidates, threshold):
    # Compute similarities
    similarities = sorted(map(lambda cand: (target.similarity(cand), cand), candidates), reverse=True)

    score, cand = similarities[0]
    if score < threshold:
        return None, score

    # TODO handle the case if there is a tiebreaker
    return cand, score


def sentiment_error(expr_sent, ground_sent):
    '''

    :param expr_sent:
    :param ground_sent:
    :return:
    '''

    return 0

# if __name__ == '__main__':
#     sent_service = Vader()
#     extractor = SpacyExtractor(sent_service)
#
#     original_doc = newsdocument.get_original_doc()
#     model_output = extractor.extract(original_doc)
#
#     ground_truth = newsdocument.get_doc()
#     print("document_error(model_output, ground_truth):")
#     print("%f" % document_error(model_output.entities, ground_truth.entities))
#
#     print("document_error(ground_truth, ground_truth):")
#     print("%f" % document_error(ground_truth.entities, ground_truth.entities))
