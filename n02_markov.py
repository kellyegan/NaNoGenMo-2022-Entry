import re
from os import walk
from os.path import basename, join
import random
from output import create_pdf, save_pdf

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


def generate_novel(source_sentences, novel_length):
    text = "".join(source_sentences)
    text_model = markovify.NewlineText(text)

    title = text_model.make_short_sentence(50)

    novel = f"# {title.rstrip('.!?')}\n\n"
    word_count = 0
    chapter_length = novel_length / 12
    chapter_min = int(chapter_length * 0.8)
    chapter_max = int(chapter_length * 1.2)

    while word_count < novel_length:
        chapter, chapter_words = generate_chapter(text_model, random.randrange(chapter_min, chapter_max))
        novel += chapter
        word_count += chapter_words

    return novel, word_count


if __name__ == '__main__':
    data_directory = "sentence_data"

    phrases = ["I will not", "I shall not", "I won't", "I shan't", "I will never", "I would never", "I would not",
               "I absolutely will not", "I definitely will not"]

    # # Collect source sentences from existing books
    # sentences = generate_source_sentences(phrases, data_directory)
    # sentences = [sentence.rstrip("\"'\n") + "\n" for sentence in sentences]
    # with open('source_sentences.txt', "w") as source_file:
    #     source_file.writelines(sentences)

    # Load source data from source file.
    with open('source_sentences.txt', "r") as source_file:
        source_data = source_file.readlines()
        novel, words = generate_novel(source_data, 50000)

        novel_pdf = create_pdf(novel)
        filename = basename(__file__).split(".")[0]
        save_pdf(novel_pdf, f"output/{filename}.pdf")
        print(words)






