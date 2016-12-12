import slovenian_press
from sklearn.metrics import f1_score


def main():
    correct_answers = slovenian_press.configuration.FileCsvReader(slovenian_press.commons.CORRECT_ANSWERS_FILE_PATH)\
        .read_columns()
    output = slovenian_press.configuration.FileCsvReader(slovenian_press.commons.OUTPUT_FILE_PATH).read_columns()

    score = f1_score([prediction for _, prediction in correct_answers.values],
                     [prediction for _, prediction in output.values], average='micro')
    print("{}%".format(round(score, 5) * 100.0))

if __name__ == '__main__':
    main()
