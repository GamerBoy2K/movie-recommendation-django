from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def indexPage(request):
    return render(request,'index.html')
# Create your views here.
