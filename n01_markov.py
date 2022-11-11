from output import create_pdf, save_pdf
import gutenbergpy.textget
import nltk
from nltk.tokenize import sent_tokenize
import os


def get_book_by_id(id):
    raw_book = gutenbergpy.textget.get_text_by_id(id)
    clean_book = gutenbergpy.textget.strip_headers(raw_book) \
        .decode("utf-8") \
        .replace('\n', ' ') \
        .replace('\r', '')
    return clean_book


if __name__ == '__main__':
    nltk.download('punkt')
    book = get_book_by_id(42108)
    sentences = sent_tokenize(book)
    for sentence in sentences:
        print(sentence)
