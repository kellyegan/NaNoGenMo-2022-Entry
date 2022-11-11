from output import create_pdf, save_pdf
import gutenbergpy.textget
import nltk
from nltk.tokenize import sent_tokenize
import os


def find_word(query, list_of_strings):
    return [s for s in list_of_strings if query in s]


def find_words(query_list, list_of_strings):
    results = []
    for s in list_of_strings:
        for query in query_list:
            if query in s:
                results.append(s)
            break;


if __name__ == '__main__':
    book = get_book_by_id(2641)
    sentences = sent_tokenize(book)
    sentences_with_no = find_word("no ", sentences)
    for sentence in sentences_with_no:
        print(sentence)
