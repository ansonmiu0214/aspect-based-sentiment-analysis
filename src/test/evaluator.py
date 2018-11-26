import spacy
from gensim.models import word2vec
import numpy as np
from sklearn.metrics import mean_squared_error


nlp = spacy.load('en_core_web_sm')


def document_error(model_output, ground_truth):
    '''

    :param model_output:
    :param ground_truth:
    :return:
    '''

    loss_score = 0

    pred_entities = model_output.entities
    ground_entities = ground_truth.enitities



    ent_tp = 0
    ent_fp = 0
    ent_fn = 0

    attr_tp = 0
    attr_fp = 0
    attr_fn = 0

    for ent in pred_entities:
        matched_entity = token_match(ent,ground_entities)
        if matched_entity is not None:
            ent_tp += 1
            for attr in ent.attributes:
                curr_tp = 0
                if token_match(attr, matched_entity.attributes):
                    curr_tp += 1
                    for expr,sent in attr.expression:
                        (diff,sent_score) = find_similar_phrase(expr,attr.expression)
                        loss_score += diff + mean_squared_error(sent_score,sent)
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

    loss_score += ent_recall + attr_recall





    '''
    
    loss_score = 0
    
    ents = model_output.entities
    t_ents = ground_truth.entities
    
    for ent in ents:
        t_ent = "find the most similar t_ent in t_ents within some threshold"
        if t_ent is None:
            loss_score += FALSE_POSITIVE_WEIGHT * 1
            continue
            
        
        # at this point, there is a similar entity
        # spaCy's word similarity returns a scalar up to 1.
        similarity = ent.similarity(t_ent)
        
        # mark that we have seen this entity in the ground truth.
        # assume some 'seen' field is initialised as False.
        t_ent.seen = True
        
        loss_score += (FALSE_POSITIVE_WEIGHT * (1 - similarity))
        
        t_attrs = t_ent.attributes
        for attr in ent.attrs:
            t_attr = "find the most similar attr in t_attrs within some threshold"
            
            if t_attr is None:
                loss_score += FALSE_POSITIVE_WEIGHT * 1
                continue
            
            
            # same drill for attributes, check for match
            similarity = attr.similarity(t_ttr)
            t_attr.seen = True
            loss_score += (FALSE_POSITIVE_WEIGHT * (1 - similarity))
            
            exprs = attr.exprs
            t_exprs = t_attr.exprs
            for expr, sent in exprs:
                t_expr, t_sent = "find the most similar expr in t_exprs within some threshold"
                
                if t_expr is None:
                    loss_score += FALSE_POSITIVE_WEIGHT * 1
                    continue
                
                similarity = expr.similarity(t_expr)
                t_expr.seen = True
                loss_score += (FALSE_POSITIVE_WEIGHT * (1 - similarity))
                
                loss_score += (MEAN_SQAURE_ERROR(sent, t_sent)
                
            for t_expr in t_exprs:
                if not t_expr.seen:
                    loss_score += FALSE_NEGATiVE_WEIGHT
        
        for t_attr t_attrs:
            if not t_attr.seen:
                loss_score += FALSE_NEGATIVE_WEiGHT
    
    for t_ent in t_ents:
        if not t_ent.seen:
            loss_score += FALSE_NEGATIVE_WEIGHT
    
    
    normaliser = "compute some normalisation factor for this sentence to ensure comparability"
    
    loss_score *= normaliser
    
    return loss_score
    '''

    return loss_score


def token_match(input, target_set):
    for token in target_set:
        text = token.text
        if input.text.lower() in text.lower() or text.lower() in input.lower():
            return token
    return None

def find_similar_phrase(phrase, phrases):

    word_set1 = phrase.split(' ')
    v1 = word2vec(word_set1[0])
    for w in word_set1[1:]:
        v1 = np.add(v1,word2vec(w))
    v1 /= len(word_set1)
    min_val = 100000000
    sent = 0
    min_phrase = None

    for (p,s) in phrases:
        word_set2 = p.split(' ')
        v2 = word2vec(word_set1[0])
        for w in word_set2[1:]:
            v2 = np.add(v2,word2vec(w))
        v2 /= len(word_set2)

        diff = np.dot(v1,v2)/((np.linalg.norm(v1)) * np.linalg.norm(v2))
        if diff < min:
            min = diff
            min_phrase = p
            sent = s

    return (sent,diff)




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
