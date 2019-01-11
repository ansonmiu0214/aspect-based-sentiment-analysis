import unittest
from unittest import mock
from unittest.mock import MagicMock

from evaluator.evaluator import Evaluator
from models import PreprocessorService, DataSourceService, ExtractorService, SentimentService


class EvaluatorTest(unittest.TestCase):
    def setUp(self):
        self.preprocessor = mock.create_autospec(spec=PreprocessorService)
        self.extractor = mock.create_autospec(spec=ExtractorService)
        self.sentiment = mock.create_autospec(spec=SentimentService)
        self.db = mock.create_autospec(spec=DataSourceService)
        self.db.list_all_documents = MagicMock(return_value=[])

        self.extractors = {
            "default": {
                "label": "Default",
                "extractor": self.extractor
            }
        }

        self.evaluator = Evaluator(preprocessor=self.preprocessor,
                                   extractors=self.extractors,
                                   sentiment_service=self.sentiment,
                                   db=self.db,
                                   default="default")

    def test_evaluator_invokes_db_on_list(self):
        docs = self.evaluator.get_all_documents()
        self.db.list_all_documents.assert_called_with()
        self.assertEqual(docs, [])

    def test_evaluator_doesnt_run_when_empty(self):
        res = self.evaluator.run_evaluator()
        self.db.list_all_documents.assert_called_with()
        self.assertIsNone(res)
