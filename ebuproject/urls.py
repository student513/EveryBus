"""ebuproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from ebuapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name = "home"),
    #path('search/<str:BusNm>/', views.search, name='search'),
    path('bus/', views.bus, name='bus'),
    path('detail/', views.detail, name='detail'),
    path('bookmark/', views.bookmark, name='bookmark'),
    path('bus_search/', views.bus_search, name='bus_search'),
    path('stop/', views.stop, name='stop')
]
