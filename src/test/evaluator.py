import spacy
import numpy as np
from sklearn.metrics import mean_squared_error

import newsdocument

from aggregator_service.average_aggregator import AverageAggregator
from data_source.VolatileSource import VolatileSource
from extractor_service.spacy_extractor import SpacyExtractor
from main import ABSA
from preprocessor_service.text_preprocessor import TextPreprocessor
from query_parser.simple_parser import SimpleParser
from sentiment_service.vader import Vader

nlp = spacy.load('en_core_web_sm')


def document_error(model_output, ground_truth):
    '''

    :param model_output:
    :param ground_truth:
    :return:
    '''

    loss_score = 0

    pred_entities = model_output.entities
    ground_entities = ground_truth.entities

    #print(pred_entities)
    for ent in ground_entities:
        print(ent.name)
    #print(ground_entities)



    ent_tp = 0
    ent_fp = 0
    ent_fn = 0

    attr_tp = 0
    attr_fp = 0
    attr_fn = 0

    for ent in pred_entities:
        matched_entity = token_match(ent,ground_entities,"E")
        if matched_entity is not None:
            ent_tp += 1
            curr_tp = 0
            for attr in ent.attributes:
                print("An attribute is %s" % attr.attribute)
                #curr_tp = 0
                matched_attribute= token_match(attr, matched_entity.attributes,"A")


                if matched_attribute is not None:
                    curr_tp += 1

                    for expr in attr.expressions:
                        diff = find_similar_phrase(expr,attr.expressions)
                        #if diff != 0:
                        print(diff)
                        loss_score += diff




                #loss_score += calculate_error(matched_attribute,attr)



            attr_tp += curr_tp
            attr_fp += len(ent.attributes) - curr_tp
            attr_fn += len(matched_entity.attributes) - curr_tp




    ent_fp += len(pred_entities) - ent_tp
    ent_fn += len(ground_entities) - ent_tp

    ent_precision = ent_tp / (ent_tp + ent_fp)
    ent_recall =  ent_tp / (ent_tp + ent_fn)

    ent_f1 = 2 * (ent_precision * ent_recall) / (ent_precision + ent_recall)


    attr_precison = attr_tp / (attr_tp + attr_fp)
    attr_recall = attr_tp / (attr_tp + attr_fn)

    attr_f1 = 2 * (attr_precison * attr_recall) / (attr_precison + attr_recall)

    print(ent_tp)
    print(ent_fn)
    print(ent_fp)

    print(attr_tp)
    print(attr_fp)
    print(attr_fn)

    print(ent_precision)
    print(ent_recall)

    loss_score += ent_f1 + attr_f1




    return loss_score


def token_match(input, target_set,type):

    input_text = ""
    original_text = ""


    if type == 'A':
        input_text = input.attribute
    else:
        input_text = input.name

    for token in target_set:
        if type == "A":
            original_text = token.attribute
        else:
            original_text = token.name
        if input_text.lower() in original_text.lower() or original_text.lower() in input_text.lower():
            return token
    return None

def calculate_error(attr1, attr2):
    if attr1 is None:
        return 2
    else:
        return abs(attr1.sentiment - attr2.sentiment)

def find_similar_phrase(phrase, phrases):

    nlp = spacy.load("en_core_web_sm")

    word_set1 = phrase.split(" ")
    word_set1 = sorted(word_set1)
    print(word_set1)
    v1 = nlp(word_set1[0])[0].vector
    offset = 0
    for w in word_set1[1:]:
        if w.strip() == '':
            offset += 1
        else:
            v1 = np.add(v1,nlp(w)[0].vector)
    #v1 /= len(word_set1) - offset

    print(v1)
    min_val = 100000000
    sent = 0
    min_phrase = None

    for p in phrases:
        word_set2 = p.split(' ')
        word_set2 = sorted(word_set2)
        print(word_set2)
        v2 = nlp(word_set1[0])[0].vector

        offset=0
        count = 0
        for w in word_set2[1:]:

            if w.strip() == '':
                offset+=1
            else:
                v2 = np.add(v2,nlp(w)[0].vector)
        #v2 /= (len(word_set2) - offset)

        if (count == 0):
            print(v2)
        #if v2 == v1:
            #print("The same")

        vector_diff = len(word_set1) - len(word_set2)
        diff = np.dot(v1,v2)/((np.linalg.norm(v1)) * np.linalg.norm(v2))

        if diff < min_val:
            min_val = diff
        count += 1



    # print("Min val is %d" % min_val)
    print(min_val)
    return min_val




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

if __name__ == '__main__':
    newsdocument.get_doc()
    sent_service = Vader()

    extractor = SpacyExtractor(sent_service)
    original_doc = newsdocument.get_original_doc()
    model_output = extractor.extract(original_doc)

    #print(document_error(model_output,newsdocument.get_doc()))


    #print(document_error(newsdocument.get_doc(),newsdocument.get_doc()))
    nlp = spacy.load("en_core_web_sm")
    print(nlp("hello")[0].vector)


