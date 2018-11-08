import spacy

if __name__ == "__main__":
    nlp = spacy.load('sample_model')

    print("Enter text: ", end="")
    text = input().strip()

    doc = nlp(text)
    print(text, doc.cats)