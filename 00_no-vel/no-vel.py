# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random

import markdown
from weasyprint import HTML, CSS


def create_no_phrase(min_nos, max_nos):
    phrase = ""
    word_count = 0
    for words in range(random.randrange(min_nos, max_nos)):
        phrase += "n" + random.choice([oString(random.randint(1, 10)), "o", "o"]) + " "
        word_count += 1
    return phrase.strip(), word_count


def create_chapter_titles(num_chapters):
    chapter_titles = []
    for i in range(0,num_chapters):
        title, title_length = create_no_phrase(1,10)
        chapter_titles.append(title.capitalize())

    return chapter_titles


def create_novel(novel_word_length=50000):
    novel = "\n\n# No-vel\n\n\n"
    word_count = 0
    chapter_word_count = 0

    chapter_titles = create_chapter_titles(10)
    target_chapter_length = novel_word_length / 10
    current_chapter_length = random.randrange(min(0, target_chapter_length - 500), max(target_chapter_length + 500, novel_word_length - word_count))
    print(current_chapter_length, word_count)

    while word_count < novel_word_length:

        new_phrase, words_in_sentence = create_no_phrase(2, 25)
        novel += new_phrase.capitalize()
        novel += random.choice(['.', '.', '.', '.', '.', '.', '.', '.', '.', '?', '?', '!'])

        word_count += words_in_sentence
        chapter_word_count += words_in_sentence

        # Add paragraph break
        if random.random() > 0.8:
            novel += "\n\n"
        else:
            novel += " "

        print(current_chapter_length, chapter_word_count)

        if chapter_word_count >= current_chapter_length:
            chapter_word_count = 0
            novel += "\n\n## " + chapter_titles.pop() + "\n\n"
            current_chapter_length = random.randrange(int(min(0, target_chapter_length - 500)),
                                                      int(max(target_chapter_length + 500, novel_word_length - word_count)))

    return novel


def oString(x):
    count = random.randint(1, x)
    max = random.randint(1, x)
    count = min(count, max)
    return "o" * count


def createPDF(novelString):
    novel_html = markdown.markdown(novelString)
    htmldoc = HTML(string=novel_html, base_url="")
    return htmldoc.write_pdf()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    novel = create_novel()
    novel_pdf = createPDF(novel)
    f = open("no-vel.pdf", "wb")
    f.write(novel_pdf)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
