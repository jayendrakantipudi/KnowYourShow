from django import forms
from . models import GENRE,language,Show


class languageForm(forms.ModelForm):

    class Meta:
        model = language
        fields = ('languages',)

class genreForm(forms.ModelForm):

    class Meta:
        model = GENRE
        fields = ('genres',)

class show_update_form(forms.ModelForm):
    class Meta:
        model = Show
        fields = ('titleName','releaseDate','storyLine','budget','BoxOfficeCollection')
