from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from parsifal_auth.models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=254)
    url = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        except User.DoesNotExist:
            pass

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'url', 'institution', 'location']

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
