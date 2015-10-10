# coding: utf-8

from django import forms
from django.contrib.auth.models import User

from parsifal.library.models import SharedFolder, Folder, Document


class FolderForm(forms.ModelForm):
    name = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control input-sm', 'autocomplete': 'off' }), 
            max_length=50, 
            required=True
        )
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all(), required=True)

    class Meta:
        model = Folder
        fields = ['name', 'user',]

    def clean(self):
        cleaned_data = super(FolderForm, self).clean()
        name = cleaned_data.get('name')
        user = cleaned_data.get('user')
        if Folder.objects.filter(name=name, user=user).exists():
            self.add_error('name', 'Folder with this name already exists.')


class SharedFolderForm(forms.ModelForm):
    class Meta:
        model = SharedFolder
        fields = ['name',]

class DocumentForm(forms.ModelForm):
    
    entry_type = forms.ChoiceField(widget=forms.Select(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), choices=Document.ENTRY_TYPES)
    title = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=255, required=False)
    author = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=500, required=False)
    abstract = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=4000, required=False)
    keywords = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=500, required=False)    
    year = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=10, required=False)
    month = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False)

    booktitle = forms.CharField(label='Book title', widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    editor = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    howpublished = forms.CharField(label='How it was published', widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    journal = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    publisher = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    pages = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)
    number = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)
    volume = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)
    edition = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)
    chapter = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)

    address = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)  
    crossref = forms.CharField(label='Cross-reference', widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    organization = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    school = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    series = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    language = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)

    bibtexkey = forms.CharField(label='BibTeX key', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=50, required=False)
    coden = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False)
    doi = forms.CharField(label='DOI', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=50, required=False)
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False)
    issn = forms.CharField(label='ISSN', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False)

    note = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)

    class Meta:
        model = Document
        fields = ['entry_type', 'title', 'author', 'abstract', 'keywords', 'year', 'month', 'booktitle', 
                'editor', 'howpublished', 'journal', 'url', 'publisher', 'pages', 'number', 'volume', 
                'edition', 'chapter', 'address', 'crossref', 'institution', 'organization', 'school', 
                'series', 'language', 'bibtexkey', 'coden', 'doi', 'isbn', 'issn', 'note']
