import slovenian_press
import sys


def main():
    training_set = slovenian_press.text.read_articles_set_from_file(
            slovenian_press.commons.TRAINING_SET_FILE_LOCATION)
    testing_set = slovenian_press.text.read_articles_set_from_file(
        slovenian_press.commons.TESTING_SET_FILE_PATH)
    best_predictions = slovenian_press.configuration.FileCsvReader(slovenian_press.commons.BEST_PREDICTIONS_FILE_PATH)\
        .read_columns()

    aggregator = slovenian_press.aggregation.PredictionsAggregator()
    aggregator.add_series([id for id, _ in best_predictions.values],
                          [prediction.strip() for _, prediction in best_predictions.values]
                          )

    for iteration in xrange(int(sys.argv[1])):
        feature_extractor = slovenian_press.learning.FeatureExtractor(training_set)
        learning_model = slovenian_press.learning.LearningModel(feature_extractor)
        aggregator.add_series(testing_set.id, learning_model.predict(testing_set))

    print('Average sureness: {}'.format(aggregator.calculate_average_sureness_for_predictions()))
    print('Average sureness for predictions:')
    print(aggregator.calculate_sureness_for_predictions())

    slovenian_press.output.save_results_to_csv_file(slovenian_press.commons.OUTPUT_FILE_PATH, aggregator)

if __name__ == '__main__':
    main()
