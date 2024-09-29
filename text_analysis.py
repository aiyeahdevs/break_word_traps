from extract_text_data import *
import json
import sys

# analyses the video transcript
def analyse(example_text, audio_len = 30, word_syl_thresh = 4, sentence_word_thresh = 60):
   
    character_count, word_count, num_of_sentenes, len_of_sentences, len_of_words, readability, syllables_in_words, syllables_in_sentences = extract(example_text)

    # syllables per second
    syl_second = sum(syllables_in_sentences)/audio_len

    # count of long words (more syllables than threshold)
    long_word_count = 0
    for s in syllables_in_words:
        if s > word_syl_thresh:
            long_word_count += 1

    # count of long sentences (more syllables than threshold)
    long_sentence_count = 0
    for s2 in syllables_in_sentences:
        if s2 > sentence_word_thresh:
            long_sentence_count += 1

    print("long words: ", long_word_count)
    # readability (can print score and grade level)
    r_score_flesch = readability[0].score
    r_grade_level_flesch = readability[0].grade_levels
    r_score_fog = readability[1].score
    r_grade_level_fog = readability[1].grade_level

    # readability (can print score and grade level)
    r_score_flesch = readability[0].score
    r_grade_level_flesch = readability[0].grade_levels[0]
    r_score_fog = readability[1].score
    r_grade_level_fog = readability[1].grade_level

    value = {
        "Liczba zbyt długich słów": long_word_count,
        "Liczba zbyt długich zdań": long_sentence_count,
        "Indeks czytelności Flescha": r_score_flesch,
        "Indeks czytelności Flescha (kategoria)": r_grade_level_flesch,
        "Współczynnik Mglistości Gunninga": r_score_fog,
        "Współczynnik Mglistości Gunninga (kategoria)": r_grade_level_fog,

    }

    return json.dumps(value, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python text_analysis.py <text_to_analyze>")
        sys.exit(1)
    
    input_text = " ".join(sys.argv[1:])
    result = analyse()
    print(result)

