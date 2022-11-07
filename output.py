import markdown
from weasyprint import HTML, CSS
import os


def create_pdf(markdown_string):
    html_string = markdown.markdown(markdown_string)
    html_doc = HTML(string=html_string, base_url="")

    css_file = "style.css"
    css_string = open(css_file, encoding="UTF-8").read()
    base_css = CSS(string=css_string)

    return html_doc.write_pdf(stylesheets=[base_css])


def save_pdf(pdf, path):
    f = open(path, "wb")
    f.write(pdf)


if __name__ == '__main__':
    pdf = create_pdf("# This is a test\n\nThis is only a test.")
    save_pdf(pdf, "output/test.pdf")