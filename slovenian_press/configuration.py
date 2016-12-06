import json
import pickle
import unicodedata
import collections

SOURCE_ARTICLE_ENCODING = 'windows-1250'
TARGET_ARTICLE_ENCODING = 'utf-8'
Article = collections.namedtuple('Article', ('id', 'text', 'category'))


class AbstractDatasourceReader(object):
    def read_json(self):
        """
        :rtype: dict
        """
        raise NotImplementedError()


class AbstractObjectPersistance(object):
    def write(self, entity):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()


class FileDatasourceReader(AbstractDatasourceReader):
    def __init__(self, file_path):
        self._file_path = file_path

    def read_json(self):
        with open(self._file_path, 'r') as f:
            return json.load(f, encoding=SOURCE_ARTICLE_ENCODING)


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
        return ArticlesSetModel(self._read_json_structure())

    def _read_json_structure(self):
        """
        :rtype: list[Article]
        """
        text_normalizer = TextNormalizer()
        return [self._extract_article_from_dict(article_dict, text_normalizer) for article_dict in self._datasource.read_json()]

    @staticmethod
    def _extract_article_from_dict(article_dict, text_normalizer):
        id = str(article_dict['id'][0])
        text = text_normalizer.normalize_text(article_dict.get('text', article_dict.get('headline'))[0])
        category = str(article_dict.get('specialCoverage', [''])[0])
        return Article(id, text, category)


class TextNormalizer(object):
    def normalize_text(self, text):
        normalized_text = self._strip_accents(text).encode(TARGET_ARTICLE_ENCODING)
        normalized_text = normalized_text.replace("\\n", ' ')
        for punctuation_character in ".?!()":
            normalized_text = normalized_text.replace(punctuation_character, '')
        return normalized_text

    def _strip_accents(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


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
