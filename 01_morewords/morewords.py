import tracery
from tracery.modifiers import base_english
import markdown
from weasyprint import HTML, CSS

# Press the green button in the gutter to run the script.


def get_words():
    words = []

    for i in range(80):
        words.append("#no#")

    for i in range(20):
        words.append("never")

    for i in range(10):
        words.append("nope")

    for i in range(5):
        words.extend(["definitely not", "absolutely not", "of course not", "under no circumstances", "no way", "naw", "not on your life"])

    words.extend(["not really", "we'll see", "maybe", "perhaps", "ehh", "I don't know", "possibly", "conceivably", "well"])

    return words


def create_grammar():
    paragraph_rules = {
        "word": get_words(),
        "no": ["no", "n#o#", "#no# #no#"],
        "o": ["o", "o", "o", "o", "o", "o", "o", "o", "oo", "o#o#", "o#o#", "o#o##o#"],
        "phrase": ["#word#", "#word#, #word#", "#word#, #word#, #word#"],
        "punctuation": [".", ".", ".", ".", ".", ".", "!"],
        "sentence": ["#phrase.capitalize##punctuation#", "#phrase.capitalize#, #phrase##punctuation#"],
        "sentences": ["#sentence#", "#sentence# #sentence#", "#sentence# #sentence# #sentence#", "#sentence# #sentences#", "#sentences# #sentences#", "#sentences# #sentences#"],
        "paragraph": "#sentences#\n",
        "origin": "#paragraph#"
    }
    grammar = tracery.Grammar(paragraph_rules)
    grammar.add_modifiers(base_english)
    return grammar


def create_paragraph(grammar):
    return grammar.flatten("#origin#")


def create_title(grammar):
    return grammar.flatten('#phrase.capitalize#')


def create_chapter(grammar, chapter_word_min=100):

    chapter = ""
    chapter_word_count = 0

    while chapter_word_count < chapter_word_min:
        paragraph = create_paragraph(grammar)
        chapter_word_count += len(paragraph.split())
        chapter += create_paragraph(grammar)

    return chapter, chapter_word_count


def create_novel(novel_word_min):
    grammar = create_grammar()
    chapter_titles = []
    word_count = 0
    novel_text = ""

    while word_count < novel_word_min:
        while True:
            chapter_title = create_title(grammar)
            if chapter_title not in chapter_titles:
                break

        word_count += len(chapter_title)
        chapter_text, chapter_word_count = create_chapter(grammar, 5000)
        word_count += chapter_word_count

        novel_text += f'## {chapter_title}\n\n'
        novel_text += f'{chapter_text}\n'

    novel_title = create_title(grammar)

    novel_title = f'# {novel_title}\n\n\n' + novel_text

    return novel_text, word_count


if __name__ == '__main__':
    novel, words = create_novel(50000)
    print(novel)
    print(words)
