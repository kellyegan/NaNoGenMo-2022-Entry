import re
from os import walk
from os.path import basename, join
import random
from output import create_pdf, save_pdf

import markovify


def find_pattern_in_list(query, list_of_strings):
    '''
    Return a list of strings that have at least one match to a regex pattern
    :param query: regex pattern to match
    :param list_of_strings: string to match against
    :return: list of strings that match the pattern
    '''
    pattern = re.compile(query, flags=re.IGNORECASE)
    return [s for s in list_of_strings if pattern.search(s)]


def find_patterns_in_list(query_list, list_of_strings):
    '''
    Return a list of strings that have at least one match to a pattern in a list of regex patterns
    :param query_list: list of regex patterns to match against
    :param list_of_strings: string to match the pattern
    :return: list of strings that match at least one of the patterns
    '''
    results = []
    for s in list_of_strings:
        for query in query_list:
            if re.search(query, s, flags=re.IGNORECASE):
                results.append(s)
                break;
    return results


def create_source_sentences(search_phrases, sentence_data_path):
    '''
    Search a directory of text files for sentences that match specific phrases
    :param search_phrases: list of phrases to search for
    :param sentence_data_path: path to search for text files (recursively searches directory)
    :return: list of sentences that match phrases
    '''
    sentences = []
    novels = 0

    for root, dirs, files in walk(sentence_data_path):
        for file in files:
            if file.endswith(".txt"):
                with open(join(root, file), "r") as f:
                    current_sentences = f.readlines()
                    negative_sentences = find_patterns_in_list(search_phrases, current_sentences)
                    if len(negative_sentences) > 0:
                        novels += 1
                    sentences.extend(negative_sentences)
    return sentences


def create_chapter(text_model, chapter_length):
    '''
    Create a chapter worth of text from markov chain model
    :param text_model: markov model from markovify
    :param chapter_length: desired number of words in chapter
    :return: tuple containing text of chapter and number of words it contains
    '''
    word_count = 0
    sentence_count = 0
    chapter = ""

    chapter_title = text_model.make_short_sentence(50)
    while True:
        if chapter_title:
            word_count += len(chapter_title.split())
            chapter += f"## {chapter_title.rstrip('.')}\n\n"
            break
        chapter_title = text_model.make_short_sentence(50)

    while word_count < chapter_length:
        sentence = text_model.make_sentence()
        if sentence is not None:
            word_count += len(sentence.split())
            chapter += sentence + " "
            sentence_count += 1
            if sentence_count > random.randrange(4,7):
                sentence_count = 0
                chapter += "\n\n"
    return chapter, word_count


def create_novel(source_sentences, novel_length):
    '''
    Generate a novel's worth of text, including chapters from a markov model
    :param source_sentences: sentences used to generate markov model
    :param novel_length: desired number of words in model
    :return: tuple containing text of novel and number of words
    '''
    text = "".join(source_sentences)
    text_model = markovify.NewlineText(text)

    word_count = 0
    chapter_length = novel_length / 12
    chapter_min = int(chapter_length * 0.8)
    chapter_max = int(chapter_length * 1.2)
    novel = ""

    title = text_model.make_short_sentence(50)
    while True:
        if title:
            word_count += len(title.split())
            novel += f"# {title.rstrip('.!?')}\n\n"
            break
        title = text_model.make_short_sentence(50)

    while word_count < novel_length:
        chapter, chapter_words = create_chapter(text_model, random.randrange(chapter_min, chapter_max))
        novel += chapter
        word_count += chapter_words

    return novel, word_count


if __name__ == '__main__':
    data_directory = "sentence_data"

    # Phrases to search for in source sentences
    phrases = ["I will not", "I shall not", "I won't", "I shan't", "I will never", "I would never", "I would not",
               "I absolutely will not", "I definitely will not"]
    # Restructure phrases into regex that look for words at the beginning of the search string
    queries = [r"^" + phrase + r"\b" for phrase in phrases]

    # Collect source sentences from existing books
    sentences = create_source_sentences(queries, data_directory)
    sentences = [sentence.rstrip("\"'\n") + "\n" for sentence in sentences]
    with open('source_sentences.txt', "w") as source_file:
        source_file.writelines(sentences)

    # Load source data from source file.
    with open('source_sentences.txt', "r") as source_file:
        source_data = source_file.readlines()
        text, words = create_novel(source_data, 50000)

        novel_pdf = create_pdf(text)
        filename = basename(__file__).split(".")[0]
        save_pdf(novel_pdf, f"output/{filename}.pdf")
        print(words)






