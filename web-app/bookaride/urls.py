from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='index/')),
    path('home/', views.home),

    path('oauth/login/', views.oauth_login),
    path('oauth/logout/', views.oauth_logout),
    path('oauth/authorize/', views.authorize),

    path('account/profile/', views.profile),
    path('index/', views.index),
    path('oauth/register/', views.MyRegisterView.as_view()),

    path('driver/search/', views.DriverSearchView.as_view()),
    path('driver/ride/<int:ride_id>/', views.DriverRideView.as_view()),
    path('driver/confirm_ride/', views.DriverConfirmRide),
]
