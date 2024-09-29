from extract_text_data import *
import json

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

    # readability (can print score and grade level)
    r_score_flesch = readability[0].score
    r_grade_level_flesch = readability[0].grade_levels
    r_score_fog = readability[1].score
    r_grade_level_fog = readability[1].grade_level

    value = {
        "long_words": long_word_count,
        "long_sentences": long_sentence_count,
        "flesch–kincaid_score": r_score_flesch,
        "flesch–kincaid_grade": r_grade_level_flesch,
        "gunning_fog_index_score": r_score_fog,
        "gunning_fog_index_grade": r_grade_level_fog,

    }
    
    return json.dumps(value)

