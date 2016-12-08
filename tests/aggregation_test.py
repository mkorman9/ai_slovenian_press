import slovenian_press.aggregation
import unittest
from assertpy import assert_that


class PredictionsAggregatorTest(unittest.TestCase):
    def setUp(self):
        self.aggregator = slovenian_press.aggregation.PredictionsAggregator()

    def test_should_add_new_series(self):
        # given
        ids = ['1', '2', '3']
        predictions = ['147', '148', '149']

        # when
        self.aggregator.add_series(ids, predictions)

        # then
        assert_that(self.aggregator.series).is_equal_to({'1': ['147'], '2': ['148'], '3': ['149']})

    def test_should_merge_collection_to_existing_series(self):
        # given
        ids = ['1', '2', '3']
        predictions1 = ['147', '148', '149']
        predictions2 = ['157', '158', '159']

        # when
        self.aggregator.add_series(ids, predictions1)
        self.aggregator.add_series(ids, predictions2)

        # then
        assert_that(self.aggregator.series).is_equal_to({'1': ['147', '157'], '2': ['148', '158'], '3': ['149', '159']})

    def test_should_calculate_most_common_elements(self):
        # given
        ids = ['1', '2', '3']
        predictions1 = ['147', '148', '149']
        predictions2 = ['157', '158', '159']
        predictions3 = ['147', '158', '149']

        # when
        self.aggregator.add_series(ids, predictions1)
        self.aggregator.add_series(ids, predictions2)
        self.aggregator.add_series(ids, predictions3)

        # then
        assert_that(self.aggregator.calculate_average_predictions()).is_equal_to({'1': '147', '2': '158', '3': '149'})

    def test_should_calculate_sureness_for_elements(self):
        # given
        ids = ['1', '2']
        predictions1 = ['147', '148']
        predictions2 = ['157', '148']

        # when
        self.aggregator.add_series(ids, predictions1)
        self.aggregator.add_series(ids, predictions2)

        # then
        assert_that(self.aggregator.calculate_sureness_for_predictions()).is_equal_to({'1': 0.5, '2': 1.0})

    def test_should_calculate_average_sureness(self):
        # given
        ids = ['1', '2']
        predictions1 = ['147', '148']
        predictions2 = ['157', '148']

        # when
        self.aggregator.add_series(ids, predictions1)
        self.aggregator.add_series(ids, predictions2)

        # then
        assert_that(self.aggregator.calculate_average_sureness_for_predictions()).is_equal_to(0.75)
