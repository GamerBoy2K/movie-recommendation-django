from django.urls import path,include
from . import views


urlpatterns=[
    path('',views.indexPage),
    path('login',views.login),
    path('signup',views.signup),
    path('search',views.search),
    path('movieDetails/<int:id>',views.movieDetails),
    path('movies/<int:pno>',views.allMovies),
   
]