from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class mform(forms.ModelForm):
    class Meta:
        model=movies
        fields="__all__"

class RegisterUserForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(max_length=100)
    last_name=forms.CharField(max_length=100)
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')