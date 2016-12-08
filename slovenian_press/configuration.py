import json
import pickle
import commons


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
