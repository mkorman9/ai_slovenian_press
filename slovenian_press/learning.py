from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.neural_network import MLPClassifier
from configuration import ArticlesSetModel


class FeatureExtractor(object):
    """ Feature extraction using Bags of Words strategy """
    def __init__(self, training_set):
        """
        :type training_set: ArticlesSetModel
        """
        self.training_set = training_set

        self.count_vectorizer = CountVectorizer()
        vocabulary = self.count_vectorizer.fit_transform(training_set.data)
        self.features_transformer = TfidfTransformer().fit(vocabulary)
        self.extracted_training_set_features = self.features_transformer.transform(vocabulary)

    def extract_features(self, dataset):
        """
        :type dataset: ArticlesSetModel
        :rtype: FeatureExtractor
        """
        extracted_vocabulary = self.count_vectorizer.transform(dataset)
        return self.features_transformer.transform(extracted_vocabulary)


class LearningModel(object):
    def __init__(self, feature_extractor):
        """
        :type feature_extractor: FeatureExtractor
        """
        self.feature_extractor = feature_extractor
        classifier = MLPClassifier()
        self.bayes_model = classifier.fit(self.feature_extractor.extracted_training_set_features,
                                          self.feature_extractor.training_set.target_names)

    def predict(self, testing_set):
        extracted_features = self.feature_extractor.extract_features(testing_set.data)
        return self.bayes_model.predict(extracted_features)
