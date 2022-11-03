# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import random

import markdown
from weasyprint import HTML, CSS


def createNovel():
    novel = "\n\n# No-vel\n\n\n"
    wordCount = 0

    while wordCount < 50000:
        novel += "N" + random.choice([oString(random.randint(1,10)), "o", "o"])
        for words in range(random.randrange(2,25)):
            novel += " n" + random.choice([oString(random.randint(1,10)), "o", "o"])
            wordCount += 1
        novel += random.choice(['.','.','.','.','.','.','.','.','.','?','?','!'])

        #Add paragraph break
        if random.random() > 0.8:
            novel += "\n\n"
        else:
            novel += " "

    return novel


def oString(x):
    count = random.randint(1,x)
    max = random.randint(1,x)
    count = min(count, max)
    return "o" * count

def createPDF(novelString):
    novel_html = markdown.markdown(novelString)
    htmldoc = HTML(string=novel_html, base_url="")
    return htmldoc.write_pdf()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    novel = createNovel()
    novel_pdf = createPDF(novel)
    f = open("no-vel.pdf", "wb")
    f.write(novel_pdf)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
