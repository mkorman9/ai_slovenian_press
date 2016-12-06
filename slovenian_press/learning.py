from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from configuration import ArticlesSetModel


class FeatureExtractor(object):
    """ Feature extraction using Bags of Words strategy """
    @staticmethod
    def fit(training_set):
        """
        :type training_set: ArticlesSetModel
        :rtype: FeatureExtractor
        """
        feature_extractor = FeatureExtractor()
        feature_extractor.training_set = training_set

        feature_extractor.count_vectorizer = CountVectorizer()
        vocabulary = feature_extractor.count_vectorizer.fit_transform(training_set.data)
        feature_extractor.features_transformer = TfidfTransformer().fit(vocabulary)
        feature_extractor.extracted_training_set_features = feature_extractor.features_transformer.transform(vocabulary)
        return feature_extractor

    def extract_features(self, dataset):
        """
        :type dataset: ArticlesSetModel
        :rtype: FeatureExtractor
        """
        extracted_vocabulary = self.count_vectorizer.transform(dataset)
        return self.features_transformer.transform(extracted_vocabulary)


class LearningModel(object):
    @staticmethod
    def fit(feature_extractor):
        """
        :type feature_extractor: FeatureExtractor
        :rtype: LearningModel
        """
        model = LearningModel()
        model.feature_extractor = feature_extractor
        model.bayes_model = MultinomialNB().fit(model.feature_extractor.extracted_training_set_features,
                                                model.feature_extractor.training_set.target_names)
        return model

    def predict(self, testing_set):
        extracted_features = self.feature_extractor.extract_features(testing_set.data)
        return self.bayes_model.predict(extracted_features)
