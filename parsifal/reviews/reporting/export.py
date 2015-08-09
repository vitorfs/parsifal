# coding: utf-8

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

def export_review_to_docx(review):
    document = Document()

    h = document.add_heading(review.title, level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph('')

    authors = []
    authors.append(review.author.profile.get_screen_name())
    for author in review.co_authors.all():
        authors.append(author.profile.get_screen_name())
    p = document.add_paragraph(', '.join(authors))
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph('')

    print review.description

    if review.description:
        document.add_paragraph(review.description)
        document.add_paragraph('')

    document.add_heading('1 PROTOCOL', level=2)

    return document