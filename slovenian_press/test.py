import configuration
import output
import commons


def main():
    testing_set = configuration.read_articles_set_from_file(commons.TESTING_SET_FILE_PATH)
    learning_model = configuration.read_entity_from_file(commons.MODEL_FILE_PATH)

    predicted = learning_model.predict(testing_set)
    output.save_results_to_csv_file(commons.OUTPUT_FILE_PATH, zip(testing_set.id, predicted))

if __name__ == '__main__':
    main()
