import sys
from jsonargparse.typing import PositiveInt
from data_juicer.utils.constant import Fields, StatsKeys

from ..base_op import OPERATORS, Deduplicator
from ..base_op import OPERATORS, Filter

@OPERATORS.register_module('sort_length_duplicator')
class SortLengthDuplicator(Deduplicator):
    """Filter to keep samples with total text length within a specific
    range and sort them by length."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sort_by_length(self, samples):
        """Sort samples by text length."""
        return sorted(samples, key=lambda x: len(x[self.text_key]))

    def process_and_sort(self, samples):
        """Process samples and sort them by text length."""
        processed_samples = [sample for sample in samples if self.process(sample)]
        sorted_samples = self.sort_by_length(processed_samples)
        return sorted_samples

    def process(self, sample):
        # Your existing process logic here
        return super().process(sample)

    def compute_stats(self, sample):
        # Your existing compute_stats logic here
        return super().compute_stats(sample)
`
