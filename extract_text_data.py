import re
from readability import Readability
import nltk
from nltk.corpus import cmudict

example_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


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


def get_readability(text):
    #print(text)
    r = Readability(text)
    #metrics = []
    #metrics.append(r.flesch_kincaid())
    #metrics.append(r.coleman_liau())
    #metrics.append(r.dale_chall())
    #metrics.append(r.ari())
    #metrics.append(r.linsear_write())
    #r.smog()
    #metrics.append(r.spache())
    return(r.flesch(),r.gunning_fog())

def count_syllables_in_words(text):
    res = text.split()
    print(res)
    nltk.download('cmudict')
    d = cmudict.dict()
    syllables_words = []
    for word in res:
        try:
            syllables_words.append(max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]))
        except KeyError:
            # Jeśli słowo nie jest w słowniku, szacujemy liczbę sylab na podstawie samogłosek
            syllables_words.append(len(''.join(c for c in word if c in 'aeiouAEIOU')))
    return(syllables_words)


def count_syllables_in_sentences(text):
    nltk.download('cmudict')
    d = cmudict.dict()
    sentences = text.split(".")
    syllables_sentences = []
    for sentence in sentences:
        syllables_words = []
        res = sentence.split()
        #print(res)

        for word in res:
            try:
                syllables_words.append(max([len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]))
            except KeyError:
                # Jeśli słowo nie jest w słowniku, szacujemy liczbę sylab na podstawie samogłosek
                syllables_words.append(len(''.join(c for c in word if c in 'aeiouAEIOU')))
        if sum(syllables_words) != 0:
            syllables_sentences.append(sum(syllables_words))
    return(syllables_sentences)

print(count_syllables_in_sentences(example_text))
