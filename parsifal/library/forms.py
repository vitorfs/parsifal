from django import forms

from parsifal.library.models import Folder


class FolderForm(forms.ModelForm):
    name = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control input-sm', 'autocomplete': 'off' }), 
            max_length=50, 
            required=True
        )

    class Meta:
        model = Folder
        fields = ['name',]
