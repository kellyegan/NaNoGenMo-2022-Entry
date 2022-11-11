from output import create_pdf, save_pdf
import gutenbergpy.textget
import nltk
from nltk.tokenize import sent_tokenize

top_hundred_id = [2641, 145, 37106, 16389, 67979, 100, 2701, 394, 6761, 2160, 4085, 6593, 1259, 5197, 84, 1342, 25344,
                  46, 345, 11, 1661, 2542, 43, 174, 69314, 64317, 1952, 98, 20228, 844, 69313, 1260, 1080, 69311, 1400,
                  23, 76, 5200, 69308, 2554, 2591, 41, 69310, 219, 408, 4300, 28054, 1232, 2600, 2852, 158, 120, 6130,
                  205, 45031, 1184, 996, 3207, 55, 1727, 768, 74, 203, 1497, 2814, 69307, 45, 58585, 16, 244, 7370, 160,
                  3825, 514, 135, 31284, 215, 1399, 35, 852, 10007, 30254, 42324, 779, 4363, 2148, 236, 69316, 20203,
                  43453, 521, 35899, 1250, 27827, 69315, 42108, 16328, 105, 730, 33283]


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
