import unicodedata
import commons


class TextProcessor(object):
    def process(self, text):
        """
        :type text: string
        :rtype: string
        """
        raise NotImplementedError()


class AccentsRemover(TextProcessor):
    def process(self, text):
        return self._strip_accents(text).replace("\n", ' ').encode(commons.TARGET_ARTICLE_ENCODING)

    def _strip_accents(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


class TextNormalizer(TextProcessor):
    def process(self, text):
        return self._convert_to_lower(
            self._remove_punctuation_signs(
                self._remove_words_shorter_than_3(
                    self._remove_digits(
                        self._remove_long_words_endings(text)
                    )
                )
            )
        ).decode(commons.TARGET_ARTICLE_ENCODING, 'replace')

    # this method FTW! Adds about 5% of performance
    def _remove_long_words_endings(self, normalized_text):
        normalized_text = ' '.join(word[:3] if len(word) > 5 else word for word in normalized_text.split(' '))
        return normalized_text

    def _remove_digits(self, normalized_text):
        normalized_text = ' '.join(word for word in normalized_text.split(' ') if not word.isdigit())
        return normalized_text

    def _remove_words_shorter_than_3(self, normalized_text):
        normalized_text = ' '.join(word for word in normalized_text.split(' ') if len(word) > 3)
        return normalized_text

    def _convert_to_lower(self, text):
        normalized_text = text.lower()
        return normalized_text

    def _remove_punctuation_signs(self, normalized_text):
        for punctuation_character in commons.PUNCTUATION_SIGNS:
            normalized_text = normalized_text.replace(punctuation_character, '')
        return normalized_text


class TextProcessingChain(TextProcessor):
    def __init__(self):
        self._chain = []

    def register(self, text_processor):
        self._chain.append(text_processor)

    def process(self, text):
        for processor in self._chain:
            text = processor.process(text)
        return text
