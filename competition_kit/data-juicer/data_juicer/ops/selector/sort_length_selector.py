
from collections import Counter

import datasets
from jsonargparse.typing import PositiveInt
from data_juicer.utils.constant import Fields, StatsKeys

from ..base_op import OPERATORS, Selector
from ..base_op import OPERATORS, Filter

def extract_value(item):
    return {'original_path':item['meta']['original_path']}


def shuffle_and_take_top_num(group,min_num):
    group = group.sample(frac=1)  # 打乱数据
    return group.head(min_num)

@OPERATORS.register_module('sort_length_selector')
class SortLengthSelector(Selector):
    """Filter to keep samples with total text length within a specific
    range and sort them by length."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def process(self, dataset):
        # Your existing process logic here

        dataset = dataset.map(extract_value, num_proc=12)["train"]
        # class_counts = dataset['Task'].value_counts()
        label_counts = Counter(dataset['original_path'])

        # 找到最小的类别样本数量
        min_count = min(label_counts.values())

        dataset_list = []

        # for dataset_name in label_counts:
        #     select_dataset = dataset.filter(lambda example: example['original_path'] ==dataset_name)
        #     dataset_list.append(select_dataset.shuffle()[:min_count])
        grouped_dataset = dataset.to_pandas().groupby("original_path")
        result_df = grouped_dataset.apply(lambda x: shuffle_and_take_top_num(x, min_count))
        balanced_dataset = datasets.Dataset.from_pandas(result_df)

        return balanced_dataset

