import xml.etree.ElementTree as ET
from src.models import DocumentComponent, PreprocessorService, Document

class TextPreprocessor(PreprocessorService):
    '''
    Simple input preprocessor, takes string input and wraps
    '''

    def preprocess(self, xml):
        document = Document()

        document.add_metadata("title", "Imported from TextPreprocessor")

        tree = ET.parse(xml)
        root = tree.getroot()

        content = ' '.join(map(lambda i: i.text, root.findall('./text/p')))
        document.add_component(DocumentComponent('content', content))

        return document


def main():
    tp = TextPreprocessor()
    with open('../444498newsML.xml') as file:
        document = tp.preprocess(file)



if __name__ == '__main__':
    main()
