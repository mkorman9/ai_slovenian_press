import configuration
import output


def main():
    testing_set = configuration.read_articles_set_from_file('../data/sta-special-articles-2015-testing.json')
    learning_model = configuration.read_entity_from_file('../model.bin')

    predicted = learning_model.predict(testing_set)
    output.save_results_to_csv_file('../output.csv', zip(testing_set.id, predicted))

if __name__ == '__main__':
    main()
