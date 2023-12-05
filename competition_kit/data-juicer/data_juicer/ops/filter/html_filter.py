from typing import List, Tuple, Union
import re
from data_juicer.utils.constant import Fields

from ..base_op import OPERATORS, Filter

def contains_html_code(text):
    # 定义匹配HTML标签的正则表达式
    html_pattern = re.compile('<.*?>')

    # 使用正则表达式查找匹配项
    matches = re.findall(html_pattern, text)

    # 如果找到匹配项，则表示包含HTML代码，返回状态为包含
    if matches:
        return True
    else:
        return False
@OPERATORS.register_module('html_filter')

class HtmlFilter(Filter):
    """Filter to keep samples with specified suffix."""

    def __init__(self,
                 *args,
                 **kwargs):
        """
        Initialization method.

        :param suffixes: the suffix of text that will be keep.
            For example: '.txt', 'txt' or ['txt', '.pdf', 'docx']
        :param args: extra args
        :param kwargs: extra args
        """
        super().__init__(*args, **kwargs)

    def compute_stats(self, sample, context=False):
        # check if it's computed already
        if StatsKeys.contains_html_code in sample[Fields.stats]:
            return sample

        contains_html = contains_html_code(sample[self.text_key])
        sample[Fields.stats][StatsKeys.contains_html_code] = contains_html
        return sample

    def process(self, sample):
        return not sample[Fields.stats][StatsKeys.contains_html_code]
