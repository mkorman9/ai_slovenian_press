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
        normalized_text = text.lower()
        for punctuation_character in commons.PUNCTUATION_SIGNS:
            normalized_text = normalized_text.replace(punctuation_character, '')
        normalized_text = ' '.join(word for word in normalized_text.split(' ') if len(word) > 3 and not word.isdigit())
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
