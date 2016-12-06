import json
import pickle

SOURCE_ARTICLE_ENCODING = 'windows-1250'
TARGET_ARTICLE_ENCODING = 'utf-8'


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
        :rtype: list[tuple[string, string, string]]
        """
        return [(str(article['id'][0]),
                 str(article.get('specialCoverage', [''])[0]),
                 self._normalize_text(article.get('text', article.get('headline'))[0]))
                for article in self._datasource.read_json()]

    def _normalize_text(self, text):
        normalized_text = text.replace("\\n", "\n").encode(TARGET_ARTICLE_ENCODING)
        return normalized_text


# Interface compatible with return type of sklearn.datasets.fetch_20newsgroups
class ArticlesSetModel(object):
    def __init__(self, input_data):
        """
        :type input_data: list[tuple[string, string, string]]
        """
        self.id = [id for id, _, _ in input_data]
        self.target_names = [category for _, category, _ in input_data]
        self.data = [data for _, _, data in input_data]


def read_articles_set_from_file(file_path):
    return ArticlesProvider(FileDatasourceReader(file_path)).provide()


def save_entity_to_file(model, output_file_path):
    FileObjectPersistance(output_file_path).write(model)


def read_entity_from_file(input_file_path):
    return FileObjectPersistance(input_file_path).read()
