import configuration
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


# use 'bags of words' strategy
def extract_text_features(training_set):
    count_vect = CountVectorizer()
    training = count_vect.fit_transform(training_set.data)
    features_transformer = TfidfTransformer().fit(training)
    return features_transformer.transform(training)


def train_model(features, categories):
    return MultinomialNB().fit(features, categories)


def main():
    #categories = configuration.read_categories_from_file('../data/sta-special-articles-2015-specialCoverageDict.csv')
    training_set = configuration.read_articles_set_from_file('../data/sta-special-articles-2015-training.json')

    features = extract_text_features(training_set)
    model = train_model(features, training_set.target_names)
    configuration.save_model(model, '../model.bin')

if __name__ == '__main__':
    main()
