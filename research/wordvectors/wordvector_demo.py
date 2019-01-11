#!/bin/python3

import numpy as np
import word2vec


def word_vector_of_sentence(sentence):
    matrix = np.asmatrix([model[word.lower()] for word in sentence])
    return matrix


if __name__ == "__main__":
    model = word2vec.load('model.bin')
    print("Loaded model.")

    print("Enter sentence: ", end="")
    sentence = input().strip().split()

    try:
        matrix = word_vector_of_sentence(sentence)
        print(type(matrix))
        print(matrix.shape)
        print(matrix)
    except KeyError:
        print("Unknown word(s) '%s'" % sentence)
