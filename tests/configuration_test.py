import slovenian_press.configuration
import unittest
from assertpy import assert_that


class ConfigurationTest(unittest.TestCase):
    def test_csv_reader(self):
        # given
        input = ['x;y', '1;2', '3;4']
        parser = slovenian_press.configuration.AbstractCsvReader()

        # when
        headers, values = parser._parse(input)

        # then
        assert_that(headers).is_equal_to(['x', 'y'])
        assert_that(values).is_equal_to([['1', '2'], ['3', '4']])
