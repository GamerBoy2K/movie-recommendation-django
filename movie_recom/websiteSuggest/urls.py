from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.indexPage),
    path('login',views.login_users),
    path('logout',views.logout_users),
    path('signup',views.register_user),
    path('searchResult',views.searchResult),
    path('search',views.search),
    path('movieDetails/<int:id>',views.movieDetails),
    path('movies/<int:pno>',views.allMovies),
    path('addMovies',views.addMovies),
    path('addMov',views.addMov),
    path('edit/<int:id>',views.editMovie),
    path('editMovFinal',views.editFinalMovie),
    path('invalidCredentials',views.invalidCredentials),
    path('adminDashboard',views.adminDashboard),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)