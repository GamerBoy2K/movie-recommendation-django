from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.indexPage),
    path('login',views.login),
    path('signup',views.signup),
    path('searchResult',views.searchResult),
    path('search',views.search),
    path('movieDetails/<int:id>',views.movieDetails),
    path('movies/<int:pno>',views.allMovies),
    path('addMovies',views.addMovies),
    path('addMov',views.addMov),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)