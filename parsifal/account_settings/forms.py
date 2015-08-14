from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

from parsifal.authentication.models import Profile

class UserEmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={ 'class': 'form-control' }), 
            max_length=254,
            help_text='This email account will not be publicly available. It is used for your Parsifal account management, such as internal notifications and password reset.')

    class Meta:
        model = User
        fields = ['email',]


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=30, required=False)
    public_email = forms.CharField(widget=forms.EmailInput(attrs={ 'class': 'form-control' }), max_length=254, required=False)
    url = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'public_email', 'url', 'institution', 'location']

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
    new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={ 'class': 'form-control' }))
