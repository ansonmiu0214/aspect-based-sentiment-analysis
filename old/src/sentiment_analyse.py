import spacy

if __name__ == "__main__":
    nlp = spacy.load('DeepLearning_training')

    print("Enter text: ", end="")
    text = input().strip()

    doc = nlp(text)
    print(text, doc.cats)