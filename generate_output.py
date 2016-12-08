import slovenian_press


def main():
    testing_set = slovenian_press.configuration.read_articles_set_from_file(
        slovenian_press.commons.TESTING_SET_FILE_PATH)
    learning_model = slovenian_press.configuration.read_entity_from_file(slovenian_press.commons.MODEL_FILE_PATH)

    results_aggregator = slovenian_press.aggregation.PredictionsAggregator()
    results_aggregator.add_series(testing_set.id, learning_model.predict(testing_set))

    slovenian_press.output.save_results_to_csv_file(slovenian_press.commons.OUTPUT_FILE_PATH, results_aggregator)

if __name__ == '__main__':
    main()
