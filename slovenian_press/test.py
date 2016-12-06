import configuration


def main():
    testing_set = configuration.read_articles_set_from_file('../data/sta-special-articles-2015-testing.json')
    learning_model = configuration.read_entity_from_file('../model.bin')

    learning_model.predict(testing_set)

if __name__ == '__main__':
    main()
