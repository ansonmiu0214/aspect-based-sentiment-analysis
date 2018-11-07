from src.models import DocumentComponent, PreprocessorService, Document


class TextPreprocessor(PreprocessorService):
    '''
    Simple input preprocessor, takes string input and wraps
    '''

    def preprocess(self, doc):
        document = Document()

        document.add_metadata("title", "Imported from TextPreprocessor")

        for paragraph in doc.strip().split('\n\n'):
            component = DocumentComponent('text', paragraph)
            document.add_component(component)

        return document
