import unittest

from preprocessor_service.text_preprocessor import TextPreprocessor


class PreprocessorTests(unittest.TestCase):
    def setUp(self):
        self.preprocessor = TextPreprocessor()

    def test_txt_preserves_content(self):
        text = "The quick brown fox jumped over the lazy dog."
        doc = self.preprocessor.preprocess(text, "txt")

        doc_text = " ".join(map(lambda e: e.text, doc.components))
        self.assertEqual(text, doc_text)

    def test_xml_preserves_content(self):
        content = "Hello, world!"
        text = '<newsitem date="2018-01-01"><text><p>' \
               + content \
               + '</p></text></newsitem>'
        doc = self.preprocessor.preprocess(text, "xml")

        doc_text = " ".join(map(lambda e: e.text, doc.components))
        self.assertEqual(content, doc_text)

    def test_unsupported_ext_returns_none(self):
        doc = self.preprocessor.preprocess("", "unsupported extension")
        self.assertIsNone(doc)
