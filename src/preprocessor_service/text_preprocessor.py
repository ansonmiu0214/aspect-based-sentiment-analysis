import xml.etree.ElementTree as ET

from models import DocumentComponent, PreprocessorService, Document


class TextPreprocessor(PreprocessorService):
    '''
    Simple input preprocessor, takes string input and wraps by extension
    '''

    def __init__(self):
        # Dictionary of callbacks (function pointers)
        self.handlers = {
            'xml': self.preprocess_xml,
            'txt': self.preprocess_txt
        }

    @staticmethod
    def concat_elements(root, tag):
        return ' '.join(map(lambda i: i.text, root.findall(tag)))

    @staticmethod
    def get_filename(doc):
        try:
            return doc.filename
        except AttributeError:
            return doc.name

    def preprocess(self, doc, ext):
        if ext not in self.handlers:
            return None

        return self.handlers[ext](doc)

    def preprocess_xml(self, text):
        document = Document()

        root = ET.fromstring(text)

        content = self.concat_elements(root, './text/p')
        document.add_component(DocumentComponent('content', content))

        document.add_metadata('title', self.concat_elements(root, './title'))
        document.add_metadata('headline', self.concat_elements(root, './headline'))
        document.add_metadata('author', self.concat_elements(root, './byline'))
        document.add_metadata('date', root.attrib['date'])

        return document

    def preprocess_txt(self, text):
        document = Document()

        document.add_component(DocumentComponent('content', text))
        return document
