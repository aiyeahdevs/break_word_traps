import re

example_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


# num of characters without spaces, special chars
def get_num_of_characters(text):
    text = re.sub('[^A-Za-z0-9]+', '', text)
    print(text)
    return len(text)

def get_num_of_words(text):
    words = text.count(" ") - 1
    return words

def get_num_of_sentences(text):
    sentences = text.count(".")
    return sentences

def get_len_of_sentences(text):
    sentences = text.split(".")
    print(sentences)
    lengths_of_sentences = []
    for sentence in sentences:
        if sentence != "":
            words = len(sentence.split())
            lengths_of_sentences.append(words)
    return(lengths_of_sentences)


def get_len_of_words(text):
    sentences = text.split(".")
    text_words =  text.split(" ")
    print(text_words)
    lengths_of_words = []
    for w in text_words:
        if w != "":
            lengths_of_words.append(len(w))
    return(lengths_of_words)


print(get_len_of_words(example_text))
