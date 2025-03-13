from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.rent, name="rent"),
    path('sartrental', views.startrental, name="startrental"),
    path('mylocker', views.mylocker, name='mylocker'),
    path('openlocker', views.openlocker, name='openlocker'),
    path('endrental', views.endrental, name='endrental'),
]
