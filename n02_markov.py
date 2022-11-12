import re
from os import walk
from os.path import isfile, join
import random

import markovify


def find_word(query, list_of_strings):
    pattern = re.compile(r"\b" + query + r"\b", flags=re.IGNORECASE)
    return [s for s in list_of_strings if pattern.search(s)]


def find_words(query_list, list_of_strings):
    results = []
    for s in list_of_strings:
        for query in query_list:
            if re.search(r"^" + query + r"\b", s, flags=re.IGNORECASE):
                results.append(s)
                break;
    return results


def generate_source_sentences(search_phrases, sentence_data_path):
    sentences = []
    novels = 0

    for root, dirs, files in walk(sentence_data_path):
        for file in files:
            if file.endswith(".txt"):
                with open(join(root, file), "r") as f:
                    current_sentences = f.readlines()
                    negative_sentences = find_words(search_phrases, current_sentences)
                    if len(negative_sentences) > 0:
                        novels += 1
                    sentences.extend(negative_sentences)
    return sentences


def generate_chapter(text_model, chapter_length):
    chapter_title = text_model.make_short_sentence(50)

    chapter = f"## {chapter_title.rstrip('.')}\n\n"
    word_count = 0
    sentence_count = 0

    while word_count < chapter_length:
        sentence = text_model.make_sentence()
        word_count += len(sentence.split())
        chapter += sentence + " "
        sentence_count += 1
        if sentence_count > random.randrange(4,7):
            sentence_count = 0
            chapter += "\n\n"
    return chapter, word_count


def generate_novel(source_sentences, novel_length):
    text = "".join(source_sentences)
    text_model = markovify.NewlineText(text)

    title = text_model.make_short_sentence(50)

    novel = f"# {title.rstrip('.!?')}\n\n"
    word_count = 0
    chapter_length = novel_length / 12
    chapter_min = int(chapter_length * 0.8)
    chapter_max = int(chapter_length * 1.2)

    chapter, chapter_words = generate_chapter(text_model, random.randrange(chapter_min, chapter_max))
    novel += chapter
    word_count += chapter_words

    return novel, word_count


if __name__ == '__main__':
    data_directory = "sentence_data"

    phrases = ["I will not", "I shall not", "I won't", "I shan't", "I will never", "I would never", "I would not",
               "I absolutely will not", "I definitely will not"]

    # Collect source sentences from existing books
    # sentences = generate_source_sentences(phrases, data_directory)
    # sentences = [sentence.rstrip("\"'") for sentence in sentences]
    # with open('source_sentences.txt', "w") as source_file:
    #     source_file.writelines(sentences)

    # Load source data from source file.
    with open('source_sentences.txt', "r") as source_file:
        sentences = source_file.readlines()
        novel, word_count = generate_novel(sentences, 50000)
        print(novel)
        print(word_count)






