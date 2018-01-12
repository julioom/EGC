# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    name = forms.CharField(label='User Name')
    
class FilmForm(forms.Form):
    id = forms.CharField(label='Film Id')
    
class GenreForm(forms.Form):
    genre = forms.CharField(label='Genre')
    
class SynopsisForm(forms.Form):
    word = forms.CharField(label='Word to search')