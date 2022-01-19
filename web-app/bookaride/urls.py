from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('home/', views.home),

    path('oauth/login/', views.oauth_login),
    path('oauth/logout/', views.oauth_logout),
    path('oauth/authorize/', views.authorize),

    path('account/profile/', views.profile),
    path('index/', views.index),
    path('oauth/register/', views.MyRegisterView.as_view()),
]
