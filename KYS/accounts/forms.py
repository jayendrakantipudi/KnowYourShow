from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import USER

class SignUpForm(UserCreationForm):
    age = forms.IntegerField()
    profilePic = forms.ImageField()
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']
