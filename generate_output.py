import slovenian_press.configuration
import slovenian_press.output
import slovenian_press.commons


def main():
    testing_set = slovenian_press.configuration.read_articles_set_from_file(
        slovenian_press.commons.TESTING_SET_FILE_PATH)
    learning_model = slovenian_press.configuration.read_entity_from_file(slovenian_press.commons.MODEL_FILE_PATH)

    predicted = learning_model.predict(testing_set)
    slovenian_press.output.save_results_to_csv_file(slovenian_press.commons.OUTPUT_FILE_PATH, zip(testing_set.id, predicted))

if __name__ == '__main__':
    main()
