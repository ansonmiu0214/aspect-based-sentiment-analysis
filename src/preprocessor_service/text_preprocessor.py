import xml.etree.ElementTree as ET
from models import DocumentComponent, PreprocessorService, Document

class TextPreprocessor(PreprocessorService):
    '''
    Simple input preprocessor, takes string input and wraps
    '''

    @staticmethod
    def concat_elements(root, tag):
        return ' '.join(map(lambda i: i.text, root.findall(tag)))

    def preprocess(self, xml):
        document = Document()

        document.add_metadata('title', 'Imported from TextPreprocessor')

        tree = ET.parse(xml)
        root = tree.getroot()

        content = self.concat_elements(root, './text/p')
        document.add_component(DocumentComponent('content', content))

        headline = self.concat_elements(root, './headline')
        document.add_component(DocumentComponent('headline', headline))

        author = self.concat_elements(root, './byline')
        document.add_metadata('author', author)

        return document
