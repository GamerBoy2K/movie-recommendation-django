from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def indexPage(request):
    return render(request,'index.html')

def movieDetails(request):
    return render(request,'movie-details.html')
# Create your views here.
