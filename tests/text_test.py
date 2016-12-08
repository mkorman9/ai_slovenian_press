import slovenian_press.text
import unittest
import mock
from assertpy import assert_that


class TextTest(unittest.TestCase):
    def test_text_processing_chain_should_call_all_processors(self):
        # given
        processor1 = mock.MagicMock(spec=slovenian_press.text.TextProcessor)
        processor2 = mock.MagicMock(spec=slovenian_press.text.TextProcessor)

        processing_chain = slovenian_press.text.TextProcessingChain()
        processing_chain.register(processor1)
        processing_chain.register(processor2)

        # when
        processing_chain.process('input_text')

        # then
        processor1.process.assert_called_once()
        processor2.process.assert_called_once()
