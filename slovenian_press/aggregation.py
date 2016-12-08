import math
import itertools


class PredictionsAggregator(object):
    def __init__(self):
        self.series = {}

    def add_series(self, ids, predictions):
        """
        :type ids: list[string]
        :type predictions: list[string]
        """
        series = {id: prediction for id, prediction in itertools.izip(ids, predictions)}
        self._merge_to_series(series)

    def calculate_average_predictions(self):
        """
        :rtype: dict[string, string]
        """
        ret = {}
        for id, predictions_list in self.series.iteritems():
            ret[id], _ = self._calculate_list_most_common_value_and_sureness(predictions_list)
        return ret

    def calculate_sureness_for_predictions(self):
        """
        :rtype: dict[string, float]
        """
        ret = {}
        for id, predictions_list in self.series.iteritems():
            _, ret[id] = self._calculate_list_most_common_value_and_sureness(predictions_list)
        return ret

    def calculate_average_sureness_for_predictions(self):
        """
        :rtype: float
        """
        sureness_sum = 0.0
        for _, predictions_list in self.series.iteritems():
            _, sureness = self._calculate_list_most_common_value_and_sureness(predictions_list)
            sureness_sum += sureness
        return sureness_sum / float(len(self.series))

    def _merge_to_series(self, series):
        for id in series.keys():
            if id not in self.series:
                self.series[id] = [series[id]]
            else:
                self.series[id].append(series[id])

    def _calculate_list_most_common_value_and_sureness(self, predictions_list):
        most_common_element, most_common_element_count, sureness = None, 0, 0.0
        for value in predictions_list:
            element_count = predictions_list.count(value)
            if element_count > most_common_element_count:
                most_common_element = value
                most_common_element_count = element_count
                sureness = float(element_count) / float(len(predictions_list))
        return most_common_element, sureness
