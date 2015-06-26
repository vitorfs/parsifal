from django import forms

from parsifal.library.models import Folder, Document


class FolderForm(forms.ModelForm):
    name = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control input-sm', 'autocomplete': 'off' }), 
            max_length=50, 
            required=True
        )

    class Meta:
        model = Folder
        fields = ['name',]

class DocumentForm(forms.ModelForm):
    
    entry_type = models.CharField('Document type', max_length=13, choices=ENTRY_TYPES, null=True, blank=True)

    title = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '1' }), max_length=255, required=False)
    author = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '1' }), max_length=500, required=False)
    abstract = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '1' }), max_length=4000, required=False)
    keywords = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '1' }), max_length=500, required=False)    
    year = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=10, required=False)

    '''journal = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField('URL', max_length=255, null=True, blank=True)
    
    publisher = models.CharField(max_length=255, null=True, blank=True)
    pages = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    booktitle = models.CharField(max_length=255, null=True, blank=True)
    chapter = models.CharField(max_length=255, null=True, blank=True)
    crossref = models.CharField('Cross-referenced', max_length=255, null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    editor = models.CharField(max_length=255, null=True, blank=True)
    howpublished = models.CharField('How it was published', max_length=255, null=True, blank=True)
    institution = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255, null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=255, null=True, blank=True)
    series = models.CharField(max_length=255, null=True, blank=True)
    publication_type = models.CharField(max_length=255, null=True, blank=True) # Type
    language = models.CharField(max_length=255, null=True, blank=True)
    annote = models.CharField(max_length=255, null=True, blank=True)

    bibtexkey = models.CharField('Bibtex key', max_length=50, null=True, blank=True)
    coden = models.CharField(max_length=255, null=True, blank=True)
    doi = models.CharField('DOI', max_length=50, null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=30, null=True, blank=True)
    issn = models.CharField('ISSN', max_length=30, null=True, blank=True)'''

    class Meta:
        model = Document
        exclude = ['created_at', 'updated_at', 'user',]