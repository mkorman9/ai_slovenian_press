import configuration
from slovenian_press.learning import FeatureExtractor, LearningModel
import commons


def main():
    training_set = configuration.read_articles_set_from_file(commons.TRAINING_SET_FILE_LOCATION)
    feature_extractor = FeatureExtractor(training_set)
    learning_model = LearningModel(feature_extractor)

    configuration.save_entity_to_file(learning_model, commons.MODEL_FILE_PATH)

if __name__ == '__main__':
    main()
