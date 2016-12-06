import configuration
from slovenian_press.learning import FeatureExtractor, LearningModel


def main():
    training_set = configuration.read_articles_set_from_file('../data/sta-special-articles-2015-training.json')
    feature_extractor = FeatureExtractor.fit(training_set)
    learning_model = LearningModel.fit(feature_extractor)

    configuration.save_entity_to_file(learning_model, '../model.bin')

if __name__ == '__main__':
    main()
