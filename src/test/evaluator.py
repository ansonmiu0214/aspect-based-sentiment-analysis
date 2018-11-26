import spacy

nlp = spacy.load('en_core_web_sm')


def document_error(model_output, ground_truth):
    '''

    :param model_output:
    :param ground_truth:
    :return:
    '''

    loss_score = 0

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
