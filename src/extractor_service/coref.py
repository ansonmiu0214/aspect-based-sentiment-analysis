import spacy

# TODO replace with a proper pronoun check
SUBJ_BLACKLIST = {'it', 'we'}


class Coreferencer:
    def __init__(self):
        self.nlp = spacy.load('en_coref_sm')

    def process(self, text: str, verbose=False) -> str:
        doc = self.nlp(text)

        if not doc._.has_coref:
            return text

        processed_text = []

        # Replace tokens part of a coreference with the main token of the coreference
        for token in doc:
            if token._.in_coref:
                main_subj_token = token._.coref_clusters[0].main
                main_subj_text = main_subj_token.text

                # Ignore coreferences that are pronouns (e.g. 'his', 'her') or are badly detected (not alphabet)
                if not main_subj_text.isalpha() or main_subj_text.lower() in SUBJ_BLACKLIST:
                    processed_text.append(token.text_with_ws)
                else:
                    if verbose:
                        print("*{}*".format(main_subj_token.text))
                    processed_text.append(main_subj_token.text_with_ws)
            else:
                processed_text.append(token.text_with_ws)

        # Join tokens and return string to caller
        return "".join(processed_text)


# def process(text):
#     nlp = spacy.load('en_coref_sm')
#     doc = nlp(text)
#
#     for token in doc:
#         if token._.in_coref:
#             print(token._.coref_clusters[0].main, end=" ")
#         else:
#             print(token, end=" ")
#
#     # print(doc._.coref_clusters)


if __name__ == '__main__':
    # text = input().strip()
    text = """\ Smartphone sales and cost savings helped BT beat market expectations for first-half earnings on 
        Thursday, with its departing chief executive saying his recovery plan was working. 

        Gavin Patterson, who is being replaced as CEO by Worldpay’s Philip Jansen in February, said BT was improving 
        customer service, accelerating the roll-out of full-fibre networks and transforming its operating model. 

        Shares in the British leader in both broadband and mobile rose by more than 10 percent after it nudged its 
        guidance for the full year higher and first-half earnings rose 2 percent. 

        “Despite increasingly competitive fixed, mobile and networking markets and continued declines in legacy products 
        there is no change in our overall outlook for the full year,” Patterson said, adding that based on current 
        trading the company expected earnings to be in the upper half of its range. 

        Citi analysts, who have a “neutral” rating on BT shares, highlighted “steady improvements in the underlying trends”.

        Patterson, who has run BT for more than five years, announced a shake-up in May to address a damaging accounting 
        scandal and a poor customer service record. 

        However, a lukewarm reaction to the strategy, which involved 13,000 job cuts, led chairman Jan du Plessis to 
        decide a leadership change was needed. 

        Patterson said the plan was working and he intended to maintain momentum as he prepared his departure.

        “We were confident of our strategy when we set it out in May and the strategy had a three-to-five year horizon,
        ” he said. 

        BT posted adjusted half-year core earnings of 3.68 billion pounds ($4.74 billion) and said it expected earnings 
        for the year to be at the upper end of its 7.3-7.4 billion pound range. 

        Adjusted revenue slipped 1 percent to 11.62 billion pounds as regulated price reductions in its broadband 
        network, which serves other operators as well as BT, and declines in its enterprise businesses offset growth in 
        consumer. 

        BT’s shares rose to 266 pence, their highest since January, but are well off a high of 5 pounds during 
        Patterson’s tenure and trade on only around a nine times forward earnings multiple. """

    # text = """BT posted adjusted half-year core earnings of 3.68 billion pounds ($4.74 billion) and said it expected earnings
    #         for the year to be at the upper end of its 7.3-7.4 billion pound range."""

    print(text)
    processed_text = Coreferencer().process(text)
    print(processed_text)
    # process(text)
