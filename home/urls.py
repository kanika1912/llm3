from django.contrib import admin
from django.urls import path, include
from home import views
from . import views
urlpatterns = [
    path('', views.index, name="home"),
    path('service', views.service, name='service'),
    path('about', views.about, name='about'),
    path('submit_message/', views.submit_message, name='submit_message'),
    path('register/', views.registration, name='register'),
    
]
