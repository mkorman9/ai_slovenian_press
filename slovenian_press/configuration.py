import json
import pickle

SOURCE_ARTICLE_ENCODING = 'windows-1250'
TARGET_ARTICLE_ENCODING = 'utf-8'


class AbstractDatasourceReader(object):
    def read_all_lines(self):
        """
        :rtype: list[string]
        """
        raise NotImplementedError()

    def read_json(self):
        """
        :rtype: dict
        """
        raise NotImplementedError()


class FileDatasourceReader(AbstractDatasourceReader):
    def __init__(self, file_path):
        self._file_path = file_path

    def read_all_lines(self):
        lines = []
        with open(self._file_path, 'r') as f:
            for line in f.readlines():
                lines.append(line)
        return lines

    def read_json(self):
        with open(self._file_path, 'r') as f:
            return json.load(f, encoding=SOURCE_ARTICLE_ENCODING)


class AbstractProvider(object):
    def __init__(self, datasource):
        """
        :type datasource: AbstractDatasourceReader
        """
        self._datasource = datasource

    def provide(self):
        raise NotImplementedError()


class CategoriesProvider(AbstractProvider):
    def provide(self):
        """
        :rtype: list[string]
        """
        return [id for id, _ in (line.split(';') for line in self._datasource.read_all_lines()[1:])]


class ArticlesProvider(AbstractProvider):
    def provide(self):
        """
        :rtype: ArticlesSetModel
        """
        return ArticlesSetModel(self._read_json_structure())

    def _read_json_structure(self):
        """
        :rtype: list[tuple[int, string]]
        """
        return [(str(article['specialCoverage'][0]), self._normalize_text(article.get('text', article.get('headline'))[0]))
                for article in self._datasource.read_json()]

    def _normalize_text(self, text):
        normalized_text = text.replace("\\n", "\n").encode(TARGET_ARTICLE_ENCODING)
        return normalized_text


# Interface compatible with return type of sklearn.datasets.fetch_20newsgroups
class ArticlesSetModel(object):
    def __init__(self, input_data):
        """
        :type input_data: list[tuple[int, string]]
        """
        self.target_names = [key for key, data in input_data]
        self.data = [data for key, data in input_data]



def read_categories_from_file(file_path):
    return CategoriesProvider(FileDatasourceReader(file_path)).provide()


def read_articles_set_from_file(file_path):
    return ArticlesProvider(FileDatasourceReader(file_path)).provide()


def save_model(model, output_file_path):
    with open(output_file_path, 'w') as f:
        pickle.dump(model, f)
