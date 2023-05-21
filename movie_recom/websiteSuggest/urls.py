from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.indexPage),
    path('loginPage',views.login_users),
    path('logoutPage',views.logout_users),
    path('signup',views.register_user),
    path('searchResult',views.searchResult),
    path('search',views.search), #debug
    path('movieDetails/<int:id>',views.movieDetails),
    path('movies/<int:pno>',views.allMovies),#Need Edit
    path('addMovies',views.addMovies), #part 1 add
    path('addMov',views.addMov), #part 2 add
    path('edit/<int:id>',views.editMovie), #part 1 edit
    path('editMovFinal',views.editFinalMovie), ##part 2 edit
    path('invalidCredentials',views.invalidCredentials), #debug
    path('adminDashboard',views.adminDashboard), #need Edit
    path('updateUser',views.update_user),##need edit
    path('editDeleteTable',views.editDelete),
    path('addWatchLater/<int:id>',views.watchLaterAdd),
    path('watchLater',views.watchLaterHistory),
    path('removeWatchLater/<int:idx>',views.deleteWatchLater),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)