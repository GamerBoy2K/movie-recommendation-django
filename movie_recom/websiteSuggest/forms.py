from django import forms
from .models import *

class mform(forms.ModelForm):
    class Meta:
        model=movies
        fields="__all__"