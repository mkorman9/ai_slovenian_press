import collections


TESTING_SET_FILE_PATH = 'data/sta-special-articles-2015-testing.json'
TRAINING_SET_FILE_LOCATION = 'data/sta-special-articles-2015-training.json'
MODEL_FILE_PATH = 'model.bin'
OUTPUT_FILE_PATH = 'output.csv'
BEST_PREDICTIONS_FILE_PATH = 'data/best_prediction.csv'
SOURCE_ARTICLE_ENCODING = 'windows-1250'
TARGET_ARTICLE_ENCODING = 'utf-8'
Article = collections.namedtuple('Article', ('id', 'text', 'category'))
PUNCTUATION_SIGNS = ".,\"'?!()-<>"
