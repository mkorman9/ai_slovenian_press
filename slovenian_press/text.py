import unicodedata
import commons
from configuration import AbstractProvider, ArticlesSetModel, FileDatasourceReader
from commons import Article


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


class ArticlesProvider(AbstractProvider):
    def provide(self):
        """
        :rtype: ArticlesSetModel
        """
        return ArticlesSetModel(self._process_data())

    def _process_data(self):
        """
        :rtype: list[Article]
        """
        text_processor = TextProcessingChain()
        text_processor.register(AccentsRemover())
        text_processor.register(TextNormalizer())

        return [self._extract_article_from_dict(article_dict, text_processor) for article_dict in self._datasource.read_json()]

    @staticmethod
    def _extract_article_from_dict(article_dict, text_processor):
        id = ArticlesProvider._extract_id_from_dict(article_dict)
        headline = ArticlesProvider._process_text(ArticlesProvider._extract_headline_from_dict(article_dict),
                                                  text_processor)
        text = ArticlesProvider._process_text(ArticlesProvider._extract_text_from_dict(article_dict),
                                              text_processor)
        keywords = ArticlesProvider._join_keywords(article_dict, text_processor)
        category = ArticlesProvider._extract_category_from_dict(article_dict)
        return Article(id, headline + ' ' + text + ' ' + keywords, category)

    @staticmethod
    def _extract_id_from_dict(article_dict):
        return str(article_dict['id'][0])

    @staticmethod
    def _extract_headline_from_dict(article_dict):
        return article_dict.get('headline')[0]

    @staticmethod
    def _extract_text_from_dict(article_dict):
        return article_dict.get('text', [u''])[0]

    @staticmethod
    def _extract_keywords_from_dict(article_dict):
        return article_dict.get('keywords')

    @staticmethod
    def _extract_category_from_dict(article_dict):
        return str(article_dict.get('specialCoverage', [''])[0])

    @staticmethod
    def _join_keywords(article_dict, text_processor):
        return ' '.join([ArticlesProvider._process_text(t, text_processor)
                         for t in ArticlesProvider._extract_keywords_from_dict(article_dict)])

    @staticmethod
    def _process_text(text, text_processor):
        return text_processor.process(text)


def read_articles_set_from_file(file_path):
    return ArticlesProvider(FileDatasourceReader(file_path)).provide()
