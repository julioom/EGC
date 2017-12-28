# -*- encoding: utf-8 -*-
from django import forms

class UserForm(forms.Form):
    id = forms.CharField(label='User Id')
    
class FilmForm(forms.Form):
    id = forms.CharField(label='Movie Id')