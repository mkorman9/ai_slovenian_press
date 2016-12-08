import slovenian_press
import sys


def main():
    training_set = slovenian_press.configuration.read_articles_set_from_file(
            slovenian_press.commons.TRAINING_SET_FILE_LOCATION)
    testing_set = slovenian_press.configuration.read_articles_set_from_file(
        slovenian_press.commons.TESTING_SET_FILE_PATH)
    best_predictions = slovenian_press.configuration.FileCsvReader(slovenian_press.commons.BEST_PREDICTIONS_FILE_PATH)\
        .read_columns()

    common_predictions_map = {id: [prediction.strip()] for id, prediction in best_predictions.values}

    for iteration in xrange(int(sys.argv[1])):
        feature_extractor = slovenian_press.learning.FeatureExtractor(training_set)
        learning_model = slovenian_press.learning.LearningModel(feature_extractor)
        predictions = {id: prediction for id, prediction in zip(testing_set.id, learning_model.predict(testing_set))}

        for article_id, prediction in predictions.iteritems():
            common_predictions_map[article_id].append(prediction)

    print(common_predictions_map)

if __name__ == '__main__':
    main()
