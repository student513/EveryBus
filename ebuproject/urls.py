from django.contrib import admin
from django.urls import path
import ebuapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',ebuapp.views.home, name='home'),
    path('stop_search/', ebuapp.views.stop_search, name = 'stop_search'),
    path('stop/<int:stationid>', ebuapp.views.stop, name='stop'),
    path('bus/<int:busid>', ebuapp.views.bus, name='bus'),
    # path('bookmark/', views.bookmark, name='bookmark'),
    path('bus_search/', ebuapp.views.bus_search, name='bus_search'),
]