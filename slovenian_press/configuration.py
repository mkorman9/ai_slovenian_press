import json


class AbstractProvider(object):
    def __init__(self, file_path):
        """
        :type file_path: string
        """
        self._file_path = file_path

    def provide(self):
        raise NotImplementedError()


class CategoriesProvider(AbstractProvider):
    def provide(self):
        """
        :rtype: list[string]
        """
        with open(self._file_path, 'r') as f:
            return [id for id, _ in (line.split(';') for line in f.readlines()[1:])]


class ArticlesProvider(AbstractProvider):
    SOURCE_ARTICLE_ENCODING = 'windows-1250'
    TARGET_ARTICLE_ENCODING = 'utf-8'

    def provide(self):
        """
        :rtype: dict[int, string]
        """
        with open(self._file_path, 'r') as f:
            structure = json.load(f, encoding=self.SOURCE_ARTICLE_ENCODING)
            return {article['specialCoverage'][0]:
                        self._normalize_text(article.get('text', article.get('headline'))[0])
                    for article in structure}

    def _normalize_text(self, text):
        normalized_text = text.replace("\\n", "\n").encode(self.TARGET_ARTICLE_ENCODING)
        return normalized_text
