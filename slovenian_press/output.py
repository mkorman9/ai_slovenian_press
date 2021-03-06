from aggregation import PredictionsAggregator


class AbstractOutputSaver(object):
    def save(self, results):
        """
        :type results: PredictionsAggregator
        """
        raise NotImplementedError()


class CsvFileOutputSaver(AbstractOutputSaver):
    def __init__(self, file_path):
        self._file_path = file_path

    def save(self, results):
        with open(self._file_path, 'w') as f:
            f.write('id;specialCoverage\n')
            for id, category in results.to_flat_structure():
                f.write('{};{}\n'.format(id, category))


def save_results_to_csv_file(file_path, results):
    CsvFileOutputSaver(file_path).save(results)
