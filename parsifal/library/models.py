# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class SharedFolder(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    users = models.ManyToManyField(User, through='Collaborator', related_name='shared_folders')

    class Meta:
        verbose_name = 'Shared Folder'
        verbose_name_plural = 'Shared Folders'
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            super(SharedFolder, self).save(*args, **kwargs)
        base_slug = slugify(self.name)
        if len(base_slug) > 0:
            base_slug = slugify(u'{0} {1}'.format(self.name, self.pk))
        else:
            base_slug = self.pk
        i = 0
        unique_slug = base_slug
        while SharedFolder.objects.filter(slug=unique_slug).exists():
            i += 1
            unique_slug = u'{0}-{1}'.format(base_slug, i)
        self.slug = unique_slug
        super(SharedFolder, self).save(*args, **kwargs)


class Collaborator(models.Model):
    READ = 'R'
    WRITE = 'W'
    ADMIN = 'A'

    ACCESS_TYPES = (
        (READ, 'Read'),
        (WRITE, 'Write'),
        (ADMIN, 'Admin'),
        )

    user = models.ForeignKey(User)
    shared_folder = models.ForeignKey(SharedFolder)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_owner = models.BooleanField(default=False)
    access = models.CharField(max_length=1, choices=ACCESS_TYPES, default=READ)

    class Meta:
        verbose_name = 'Collaborator'
        verbose_name_plural = 'Collaborators'

    def save(self, *args, **kwargs):
        if self.is_owner:
            self.access = Collaborator.ADMIN
        super(Collaborator, self).save(*args, **kwargs)


class Document(models.Model):
    ARTICLE = 'article'
    BOOK = 'book'
    BOOKLET = 'booklet'
    CONFERENCE = 'conference'
    INBOOK = 'inbook'
    INCOLLECTION = 'incollection'
    INPROCEEDINGS = 'inproceedings'
    MANUAL = 'manual'
    MASTERSTHESIS = 'mastersthesis'
    MISC = 'misc'
    PHDTHESIS = 'phdthesis'
    PROCEEDINGS = 'proceedings'
    TECHREPORT = 'techreport'
    UNPUBLISHED = 'unpublished'

    ENTRY_TYPES = (
        (ARTICLE, 'Article'),
        (BOOK, 'Book'),
        (BOOKLET, 'Booklet'),
        (CONFERENCE, 'Conference'),
        (INBOOK, 'Inbook'),
        (INCOLLECTION, 'Incollection'),
        (INPROCEEDINGS, 'Inproceedings'),
        (MANUAL, 'Manual'),
        (MASTERSTHESIS, 'Master\'s Thesis'),
        (MISC, 'Misc'),
        (PHDTHESIS, 'Ph.D. Thesis'),
        (PROCEEDINGS, 'Proceedings'),
        (TECHREPORT, 'Tech Report'),
        (UNPUBLISHED, 'Unpublished'),
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
    user = models.ForeignKey(User, null=True, related_name='documents')
    review = models.ForeignKey('reviews.Review', null=True, related_name='documents')
    shared_folder = models.ForeignKey(SharedFolder, null=True, related_name='documents')

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
    document = models.ForeignKey(Document, related_name='files')
    document_file = models.FileField(upload_to='library/')
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
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, related_name='library_folders')
    documents = models.ManyToManyField(Document)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'
        ordering = ('name',)
        unique_together = (('name', 'user'),)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        if len(base_slug) > 0:
            unique_slug = base_slug
        else:
            base_slug = unique_slug = 'untitled-folder'
        i = 0
        while Folder.objects.filter(slug=unique_slug).exists():
            i += 1
            unique_slug = u'{0}-{1}'.format(base_slug, i)
        self.slug = unique_slug
        super(Folder, self).save(*args, **kwargs)
