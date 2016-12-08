import slovenian_press
from slovenian_press.learning import FeatureExtractor, LearningModel


def main():
    training_set = slovenian_press.text.read_articles_set_from_file(
        slovenian_press.commons.TRAINING_SET_FILE_LOCATION)
    feature_extractor = FeatureExtractor(training_set)
    learning_model = LearningModel(feature_extractor)

    slovenian_press.configuration.save_entity_to_file(learning_model, slovenian_press.commons.MODEL_FILE_PATH)

if __name__ == '__main__':
    main()
