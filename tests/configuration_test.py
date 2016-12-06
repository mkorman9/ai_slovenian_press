import slovenian_press.configuration
import unittest
import mock
from assertpy import assert_that


class ConfigurationTest(unittest.TestCase):
    def test_categories_should_be_retrieved_from_empty_datasource(self):
        self._test_categories_provider([], [])

    def test_categories_should_be_retrieved_from_datasource_with_just_header(self):
        self._test_categories_provider(['x;y'], [])

    def test_categories_should_be_retrieved_from_valid_datasource(self):
        self._test_categories_provider(['x;y', '1;one', '2;two', '3;three'], ['1', '2', '3'])

    def test_articles_should_be_retrieved_from_empty_datasource(self):
        self._test_articles_provider([], [], [])

    def test_articles_should_be_retrieved_from_datasource_with_single_record(self):
        self._test_articles_provider([{'specialCoverage': [123], 'text': ['xyz']}],
                                     ['123'], ['xyz'])

    def test_articles_should_be_retrieved_from_datasource_with_multiple_records(self):
        self._test_articles_provider([{'specialCoverage': [123], 'text': ['xyz']},
                                      {'specialCoverage': [666], 'text': ['zyx']}],
                                     ['123', '666'], ['xyz', 'zyx'])

    def test_articles_should_be_retrieved_from_datasource_with_record_with_no_text_field(self):
        self._test_articles_provider([{'specialCoverage': [123], 'headline': ['xyz']}],
                                     ['123'], ['xyz'])

    def _test_categories_provider(self, input, expected_output):
        # given
        datasource_mock = mock.MagicMock(spec=slovenian_press.configuration.AbstractDatasourceReader)
        datasource_mock.read_all_lines.return_value = input

        categories_provider = slovenian_press.configuration.CategoriesProvider(datasource_mock)

        # when
        result = categories_provider.provide()

        # then
        assert_that(result).is_equal_to(expected_output)

    def _test_articles_provider(self, input, expected_target_names, expected_data):
        # given
        datasource_mock = mock.MagicMock(spec=slovenian_press.configuration.AbstractDatasourceReader)
        datasource_mock.read_json.return_value = input

        articles_provider = slovenian_press.configuration.ArticlesProvider(datasource_mock)

        # when
        result = articles_provider.provide()

        # then
        assert_that(result.target_names).is_equal_to(expected_target_names)
        assert_that(result.data).is_equal_to(expected_data)
