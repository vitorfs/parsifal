# coding: utf-8

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def export_review_to_docx(review):
    document = Document()

    h = document.add_heading(review.title, level=1)
    h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph('')

    authors = list()
    authors.append(review.author.profile.get_screen_name())
    for author in review.co_authors.all():
        authors.append(author.profile.get_screen_name())
    p = document.add_paragraph(', '.join(authors))
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph('')

    if review.description:
        document.add_paragraph(review.description)

    document.add_heading('1 Protocol', level=2)

    if review.objective:
        document.add_paragraph(review.objective)

    document.add_heading('1.1 PICOC', level=3)

    p = document.add_paragraph('', style='List Bullet')
    p.add_run('Population: ').bold = True
    p.add_run(review.population)

    p = document.add_paragraph('', style='List Bullet')
    p.add_run('Intervention: ').bold = True
    p.add_run(review.intervention)

    p = document.add_paragraph('', style='List Bullet')
    p.add_run('Comparison: ').bold = True
    p.add_run(review.comparison)

    p = document.add_paragraph('', style='List Bullet')
    p.add_run('Outcome: ').bold = True
    p.add_run(review.outcome)

    p = document.add_paragraph('', style='List Bullet')
    p.add_run('Context: ').bold = True
    p.add_run(review.context)

    document.add_heading('1.2 Research Questions', level=3)
    for question in review.research_questions.all():
        document.add_paragraph(question.question, style='List Number')

    return document
