import configuration
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


def extract_test_text_features(testing_set):
    count_vect = CountVectorizer()
    testing = count_vect.transform(testing_set.data)
    features_transformer = TfidfTransformer().fit(testing)
    return features_transformer.transform(testing)


def main():
    #categories = configuration.read_categories_from_file('../data/sta-special-articles-2015-specialCoverageDict.csv')
    testing_set = configuration.read_articles_set_from_file('../data/sta-special-articles-2015-testing.json')
    model = configuration.read_model('../model.bin')
    features = extract_test_text_features(testing_set)

    model.predict(features)

if __name__ == '__main__':
    main()
