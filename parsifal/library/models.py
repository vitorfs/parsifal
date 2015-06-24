from django.db import models

class Document(models.Model):

    ARTICLE = u'article'
    BOOK = u'book'
    BOOKLET = u'booklet'
    CONFERENCE = u'conference'
    INBOOK = u'inbook'
    INCOLLECTION = u'incollection'
    INPROCEEDINGS = u'inproceedings'
    MANUAL = u'manual'
    MASTERSTHESIS = u'mastersthesis'
    MISC = u'misc'
    PHDTHESIS = u'phdthesis'
    PROCEEDINGS = u'proceedings'
    TECHREPORT = u'techreport'
    UNPUBLISHED = u'unpublished'

    ENTRY_TYPES = (
        (ARTICLE, u'Article'),
        (BOOK, u'Book'),
        (BOOKLET, u'Booklet'),
        (CONFERENCE, u'Conference'),
        (INBOOK, u'Inbook'),
        (INCOLLECTION, u'Incollection'),
        (INPROCEEDINGS, u'Inproceedings'),
        (MANUAL, u'Manual'),
        (MASTERSTHESIS, u'Master\'s Thesis'),
        (MISC, u'Misc'),
        (PHDTHESIS, u'Ph.D. Thesis'),
        (PROCEEDINGS, u'Proceedings'),
        (TECHREPORT, u'Tech Report'),
        (UNPUBLISHED, u'Unpublished'),
        )

    # Bibtex required fields
    entry_type = models.CharField(max_length=13, choices=ENTRY_TYPES)
    bibtexkey = models.CharField(max_length=50)

    # Bibtex base fields
    address = models.CharField(max_length=255, null=True, blank=True)
    annote = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    booktitle = models.CharField(max_length=255, null=True, blank=True)
    chapter = models.CharField(max_length=255, null=True, blank=True)
    crossref = models.CharField(max_length=255, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    editor = models.CharField(max_length=255, null=True, blank=True)
    howpublished = models.CharField(max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    journal = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255, null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    series = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    publication_type = models.CharField(max_length=255, null=True, blank=True) # Type
    volume = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)

    # Extra fields

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __unicode__(self):
        return self.title

