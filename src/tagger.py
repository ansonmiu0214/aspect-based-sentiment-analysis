import sys
from nltk import sent_tokenize

def load_file():
    file = open(sys.argv[1], 'a')
    return file

def tokenize(file):
    return sent_tokenize(file)

def label_text(sentences):
    #print sentence
    #take input from user for indexes for <E#A,A>
    #Append spacy format label to file

