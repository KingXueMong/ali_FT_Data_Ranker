import unittest
from data_juicer.ops.selector import BalancedSelector
from datasets import Dataset


class TextLengthFilterTest(unittest.TestCase):

    def test_func1(self):
        ds_list = {'original_path': ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C']}
        tgt_list = {'original_path': ['A', 'A', 'B', 'B',  'C', 'C']}
        ds_dataset = Dataset.from_dict(ds_list)
        tgt_dataset = Dataset.from_dict(tgt_list)
        op = BalancedSelector(field_key='meta.suffix')
        self.assertEqual(tgt_dataset.to_list(), op.to_list())

    def test_func2(self):
        pass

    def test_func3(self):
        pass