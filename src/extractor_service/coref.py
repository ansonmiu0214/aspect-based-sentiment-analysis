import spacy

SUBJ_BLACKLIST = {'it', 'we'}
SUBJ_POSSESSION = {'its', 'their'}


class Coreferencer:
    '''
    Research exploration into using an external coreference resolution library
    to perform the textual replacements that improve performance of the extractor.
    '''
    def __init__(self):
        self.nlp = spacy.load('en_coref_sm')

    def process(self, text: str, verbose=False) -> str:
        '''
        String-to-string coreference resolution through textual replacements.
        '''
        doc = self.nlp(text)

        if not doc._.has_coref:
            return text

        processed_text = []
        if verbose:
            print("Coreferencing replacements:")

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

                    # Include a possession mark if originally a possessive.
                    replacement = main_subj_text
                    if token.text.lower() in SUBJ_POSSESSION:
                        replacement += "'s"

                    # Correct for whitespace
                    if token.text_with_ws.endswith(' '):
                        replacement += ' '

                    processed_text.append(replacement)
            else:
                processed_text.append(token.text_with_ws)

        if verbose:
            print()

        # Join tokens and return string to caller
        return "".join(processed_text)