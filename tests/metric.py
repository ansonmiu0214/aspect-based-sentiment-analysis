import unittest
from evaluator.metric import *

from models import EntityEntry, AttributeEntry, ExpressionEntry


ent1 = EntityEntry("mexico")
ent1.add_attribute(AttributeEntry("economy", expressions=[
    ExpressionEntry("mexico's economy is great", sentiment=1)
]))


ent2 = EntityEntry("apple")
ent2.add_attribute(AttributeEntry("iphone", expressions=[
    ExpressionEntry("apple's iphone sales decreased last month", sentiment=-0.5)
]))


ent3 = EntityEntry("mexico")
ent3.add_attribute(AttributeEntry("economy", expressions=[
    ExpressionEntry("mexico's economy is great", sentiment=0)
]))


class MetricTests(unittest.TestCase):

    def test_same_doc_returns_optimal_scores(self):
        model_output = [ent1]
        ground_truth = [ent1]
        scores_dict = document_error(model_output,ground_truth)
        self.assertEqual(scores_dict['ent_f1'],1)
        self.assertEqual(scores_dict['attr_f1'],1)
        self.assertEqual(scores_dict['mse'],0)

    def test_diff_docs_return_sub_optimal_scores(self):
        model_output = [ent1]
        ground_truth = [ent2]
        scores_dict = document_error(model_output,ground_truth)
        self.assertLess(scores_dict['ent_f1'], 1)
        self.assertLess(scores_dict['attr_f1',1])

    def test_no_extraction_gives_neagtive_one_for_mse(self):
        model_output = [ent1]
        ground_truth = [ent2]
        scores_dict = document_error(model_output,ground_truth)
        self.assertEqual(scores_dict['mse'],-1)


    def test_greater_than_zero_mse_for_different_docs(self):
        model_output = [ent1]
        ground_truth = [ent3]
        scores_dict = document_error(model_output,ground_truth)
        self.assertGreater(scores_dict['mse'],0)






