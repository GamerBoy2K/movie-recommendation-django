from django.urls import path,include
from . import views


urlpatterns=[
    path('',views.indexPage),
    path('movieDetails',views.movieDetails),
    path('login',views.login),
   
]