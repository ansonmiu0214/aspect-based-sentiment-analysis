import xml.etree.ElementTree as ET
from models import DocumentComponent, PreprocessorService, Document

class TextPreprocessor(PreprocessorService):
    '''
    Simple input preprocessor, takes string input and wraps
    '''

    @staticmethod
    def concat_elements(root, tag):
        return ' '.join(map(lambda i: i.text, root.findall(tag)))

    @staticmethod
    def get_filename(doc):
        try:
            return doc.filename
        except AttributeError:
            return doc.name

    def preprocess(self, doc):
        document = Document()

        # For plaintext input
        if isinstance(doc, str):
            document.add_component(DocumentComponent('content', doc))
            return document

        document.add_metadata('title', 'Imported from TextPreprocessor')

        if self.get_filename(doc).endswith(".xml"):
            tree = ET.parse(doc)
            root = tree.getroot()

            content = self.concat_elements(root, './text/p')
            document.add_component(DocumentComponent('content', content))

            headline = self.concat_elements(root, './headline')
            document.add_component(DocumentComponent('headline', headline))

            author = self.concat_elements(root, './byline')
            document.add_metadata('author', author)
        else:
            content = doc.read().decode('utf-8')
            document.add_component(DocumentComponent('content', content))

        return document
