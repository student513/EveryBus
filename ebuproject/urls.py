from django.contrib import admin
from django.urls import path
import ebuapp.views
import accounts.views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ebuapp.views.home, name='home'),
    path('stop_search/', ebuapp.views.stop_search, name = 'stop_search'),
    path('stop/<int:stationid>', ebuapp.views.stop, name='stop'),
    path('bus/<int:busid>', ebuapp.views.bus, name='bus'),
    # path('bookmark/', views.bookmark, name='bookmark'),
    path('bus_search/', ebuapp.views.bus_search, name='bus_search'),

    path('signup/',accounts.views.signup, name='signup'),
    path('login/', accounts.views.login, name='login'),  
    path('logout/', accounts.views.logout, name='logout'),
    path('stop/<int:stationid>/<int:busid>/<busname>/book_bus/', ebuapp.views.book_bus, name='book_bus'),
    path('bus/<int:busid>/<int:stationid>/<stationname>/book_stop/', ebuapp.views.book_stop, name='book_stop'),
    path('bookmark/', ebuapp.views.bookmark, name='bookmark'),
]