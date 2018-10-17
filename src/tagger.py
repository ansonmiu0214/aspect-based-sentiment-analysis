import sys
from nltk import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')

def get_data():
    file = open(sys.argv[1])
    data = file.read()
    return data

def tokenize(file):
    return sent_tokenize(file)

def label_text(sentences,data_file):

    print(len(sentences))
    for sentence in sentences:
        labels = []
        print(sentence)
        words = word_tokenize(sentence[:-1])
        #words = re.split(' |,', sentence[:-1])
        words = filter(lambda x: x not in [',',';',':','\'s'], words)
        for word in words:
            print(word)
            label = input("").upper()
            if (label == 'E' or label == 'A' or label == 'S'):
                labels.append(label)
            else:
                labels.append('-')
        data_file.write('/s\n')
        data_file.write(sentence + '\n')
        data_file.write('/l\n')
        for label in labels:
            data_file.write(label + '\n')
        data_file.write('/l\n')

if __name__ == "__main__":
    data_file = open(sys.argv[2], 'a')
    data = get_data()
    sentences = tokenize(data)
    label_text(sentences, data_file)



