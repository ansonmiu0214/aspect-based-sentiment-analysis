import spacy


def data_clean(path):
    file = open(path)
    nlp = spacy.load('en')
    docx = nlp(file.readlines())
    data_cleaned = [word for word in docx if not word.is_stop and not word.is_punct]
    print(data_cleaned)


if __name__ == '__main__':
    data_clean("test.ft.txt")
