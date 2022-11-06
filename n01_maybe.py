import random

from output import create_pdf, save_pdf
from os import path
import tracery
from tracery.modifiers import base_english


# Press the green button in the gutter to run the script.


def create_wordlist():
    words = []

    negatives = ["definitely not", "absolutely not", "of course not", "under no circumstances", "no way", "no way, no how", "naw", "not on your life", "uh uh", "negative", "when pigs fly", "when hell freezes over"]
    maybes = ["meh", "ehh", "I don't know", "possibly", "conceivably", "supposedly", "well...", "not really", "we'll see", "maybe", "perhaps", "mmmm", "errrr"]
    positives = ["yeah", "alright", "technically your right", "ok", "I guess", "sure", "go ahead", "if you have to", "in certain circumstances", "if you put it that way"]

    for i in range(85):
        words.append("#no#")

    for i in range(25):
        words.append("never")

    for i in range(12):
        words.append("nope")

    for i in range(6):
        words.extend(negatives)

    random.shuffle(words)

    for i in range(5):
        words.extend(maybes)

    for i in range(5):
        words.extend(positives)

    return words


def create_grammar(words):
    paragraph_rules = {
        "word": words,
        "no": ["no", "n#o#", "#no# #no#"],
        "o": ["o", "o", "o", "o", "o", "o", "o", "o", "oo", "o#o#", "o#o#", "o#o##o#"],
        "phrase": ["#word#", "#word#, #word#", "#word#, #word#, #word#"],
        "punctuation": [".", ".", ".", ".", ".", ".", "!"],
        "sentence": ["#phrase.capitalize##punctuation#", "#phrase.capitalize#, #phrase##punctuation#"],
        "origin": "#sentence#"
    }
    grammar = tracery.Grammar(paragraph_rules)
    grammar.add_modifiers(base_english)
    return grammar


def create_sentence(grammar):
    return grammar.flatten("#origin#")


def create_title(grammar):
    return grammar.flatten('#phrase.capitalize#')


def create_chapter(grammar, chapter_word_min=100):

    chapter = ""
    chapter_word_count = 0

    while chapter_word_count < chapter_word_min:
        paragraph = create_sentence(grammar)
        chapter_word_count += len(paragraph.split())
        chapter += create_sentence(grammar) + "\n\n"

    return chapter, chapter_word_count


def create_novel(novel_word_min):
    words = create_wordlist()
    grammar = create_grammar(words[:100])

    chapter_title = create_title(grammar)
    chapter_titles = [chapter_title]
    print(chapter_title)

    word_count = 0
    novel_text = ""
    sentence_count = 0
    current_paragraph = []
    current_chapter = []

    min_chapter_length = novel_word_min / 10
    chapter_word_count = 0

    while word_count < novel_word_min:
        sentence = create_sentence(grammar)
        words_in_sentence = len(sentence.split())
        word_count += words_in_sentence
        chapter_word_count += words_in_sentence

        sentence_count += 1
        current_paragraph.append(sentence)

        # Paragraph should be between 3, 7 sentences
        if len(current_paragraph) > random.randrange(3, 7):
            current_chapter.append(" ".join(current_paragraph))
            current_paragraph = []

        # Chapters should be match approximate word length
        if chapter_word_count > random.randrange(int(min_chapter_length * 0.75), int(min_chapter_length * 1.5)):
            novel_text += f"\n\n## {chapter_title}\n\n"
            novel_text += "\n\n".join(current_chapter)
            current_chapter = []

            chapter_word_count = 0

            # Check chapter titles are unique
            while True:
                chapter_title = create_title(grammar)
                if chapter_title not in chapter_titles:
                    break
            chapter_titles.append(chapter_title)

        if sentence_count % 40 == 0:
            words.pop(0)
            grammar = create_grammar(words[:100])

    if len(current_paragraph) > 0:
        current_chapter.append(" ".join(current_paragraph))

    if len(current_chapter) > 0:
        novel_text += "\n\n".join(current_chapter)

    novel_text += "\n\nYes.\n\n"
    print(chapter_titles)

    return novel_text, word_count


if __name__ == '__main__':
    novel, words = create_novel(50000)
    novel_pdf = create_pdf(novel)
    filename = path.basename(__file__).split(".")[0]
    save_pdf(novel_pdf, f"output/{filename}.pdf")
    # print(words)
