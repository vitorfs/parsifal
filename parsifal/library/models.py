from django.db import models
from django.contrib.auth.models import User


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
    bibtexkey = models.CharField('Bibtex key', max_length=255, null=True, blank=True)
    entry_type = models.CharField('Document type', max_length=13, choices=ENTRY_TYPES, null=True, blank=True)
    
    # Bibtex base fields
    address = models.CharField(max_length=2000, null=True, blank=True)
    author = models.TextField(max_length=1000, null=True, blank=True)
    booktitle = models.CharField(max_length=1000, null=True, blank=True)
    chapter = models.CharField(max_length=1000, null=True, blank=True)
    crossref = models.CharField('Cross-referenced', max_length=1000, null=True, blank=True)
    edition = models.CharField(max_length=1000, null=True, blank=True)
    editor = models.CharField(max_length=1000, null=True, blank=True)
    howpublished = models.CharField('How it was published', max_length=1000, null=True, blank=True)
    institution = models.CharField(max_length=1000, null=True, blank=True)
    journal = models.CharField(max_length=1000, null=True, blank=True)
    month = models.CharField(max_length=50, null=True, blank=True)
    note = models.CharField(max_length=2000, null=True, blank=True)
    number = models.CharField(max_length=1000, null=True, blank=True)
    organization = models.CharField(max_length=1000, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    publisher = models.CharField(max_length=1000, null=True, blank=True)
    school = models.CharField(max_length=1000, null=True, blank=True)
    series = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    publication_type = models.CharField(max_length=1000, null=True, blank=True) # Type
    volume = models.CharField(max_length=1000, null=True, blank=True)
    year = models.CharField(max_length=50, null=True, blank=True)

    # Extra fields
    abstract = models.TextField(max_length=4000, null=True, blank=True)
    coden = models.CharField(max_length=1000, null=True, blank=True)
    doi = models.CharField('DOI', max_length=255, null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=255, null=True, blank=True)
    issn = models.CharField('ISSN', max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=2000, null=True, blank=True)
    language = models.CharField(max_length=1000, null=True, blank=True)
    url = models.CharField('URL', max_length=1000, null=True, blank=True)

    # Parsifal management field
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __unicode__(self):
        return self.title

def document_file_upload_to(instance, filename):
    return u'library/{0}/'.format(instance.document.user.pk)


class DocumentFile(models.Model):
    document = models.ForeignKey(Document)
    document_file = models.FileField(upload_to=document_file_upload_to)
    filename = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        verbose_name = 'Document File'
        verbose_name_plural = 'Document Files'

    def __unicode__(self):
        return self.filename


class Folder(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55)
    user = models.ForeignKey(User, related_name='library_folders')
    documents = models.ManyToManyField(Document)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'
        ordering = ('name',)

    def __unicode__(self):
        return self.name
