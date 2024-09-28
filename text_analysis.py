from extract_text_data import *

# TODO fix hardcoded values
audio_len = 30 # seconds
word_syl_thresh = 4
sentence_word_thresh = 60


example_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


def analyse(example_text, audio_len, word_syl_thresh, sentence_word_thresh):

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
    #print(r_score, r_grade_level[0])
    r_score_fog = readability[1].score
    r_grade_level_fog = readability[1].grade_level

    return(long_word_count, long_sentence_count, r_score_flesch, r_grade_level_flesch, r_score_fog, r_grade_level_fog)

print(analyse(example_text, audio_len, word_syl_thresh, sentence_word_thresh))




