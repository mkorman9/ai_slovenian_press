import json
import pickle
import commons
import text
from commons import Article


class AbstractDatasourceReader(object):
    def read_json(self):
        """
        :rtype: dict
        """
        raise NotImplementedError()


class FileDatasourceReader(AbstractDatasourceReader):
    def __init__(self, file_path):
        self._file_path = file_path

    def read_json(self):
        with open(self._file_path, 'r') as f:
            return json.load(f, encoding=commons.SOURCE_ARTICLE_ENCODING)


class CsvStructure(object):
    def __init__(self, headers, values):
        """
        :type headers: list[string]
        :type values: list[list[string]]
        """
        self.headers = headers
        self.values = values


class AbstractCsvReader(object):
    def read_columns(self):
        """
        :rtype: CsvStructure
        """
        raise NotImplementedError()

    def _parse(self, all_rows):
        headers = self._split(all_rows[0])
        values = [self._split(line) for line in all_rows[1:]]
        return headers, values

    def _split(self, line):
        return line.split(';')


class FileCsvReader(AbstractCsvReader):
    def __init__(self, file_path):
        self._file_path = file_path

    def read_columns(self):
        with open(self._file_path, 'r') as f:
            headers, values = self._parse(f.readlines())
            return CsvStructure(headers, values)


class AbstractObjectPersistance(object):
    def write(self, entity):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()


class FileObjectPersistance(AbstractObjectPersistance):
    def __init__(self, file_path):
        self._file_path = file_path

    def write(self, entity):
        with open(self._file_path, 'w') as f:
            pickle.dump(entity, f)

    def read(self):
        with open(self._file_path, 'r') as f:
            return pickle.load(f)


class AbstractProvider(object):
    def __init__(self, datasource):
        """
        :type datasource: AbstractDatasourceReader
        """
        self._datasource = datasource

    def provide(self):
        raise NotImplementedError()


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
        text_processor = text.TextProcessingChain()
        text_processor.register(text.AccentsRemover())
        text_processor.register(text.TextNormalizer())

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


# Interface compatible with return type of sklearn.datasets.fetch_20newsgroups
class ArticlesSetModel(object):
    def __init__(self, input_data):
        """
        :type input_data: list[Article]
        """
        self.id = [article.id for article in input_data]
        self.target_names = [article.category for article in input_data]
        self.data = [article.text for article in input_data]


def read_articles_set_from_file(file_path):
    return ArticlesProvider(FileDatasourceReader(file_path)).provide()


def save_entity_to_file(model, output_file_path):
    FileObjectPersistance(output_file_path).write(model)


def read_entity_from_file(input_file_path):
    return FileObjectPersistance(input_file_path).read()
