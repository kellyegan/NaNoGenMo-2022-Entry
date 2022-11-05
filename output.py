import markdown
from weasyprint import HTML, CSS


def create_pdf(markdown_string):
    html_string = markdown.markdown(markdown_string)
    html_doc = HTML(string=html_string, base_url="")
    return html_doc.write_pdf()


def save_pdf(pdf, path):
    f = open(path, "wb")
    f.write(pdf)


if __name__ == '__main__':
    pdf = create_pdf("# This is a test\n\nThis is only a test.")
    save_pdf(pdf, "output/test.pdf")