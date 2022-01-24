from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
     path('', RedirectView.as_view(url='index/')),
    path('home/', views.home),

    path('oauth/login/', views.oauth_login),
    path('oauth/logout/', views.oauth_logout),
    path('oauth/authorize/', views.authorize),

    path('account/profile/', views.profile),
    path('index/', views.index),
    path('oauth/register/', views.MyRegisterView.as_view()),

    path('driver/register', views.MyRegisterAsDerverView.as_view()),
    path('account/modifyvehicle', views.ModifyVehicleView.as_view()),

    path('account/change-password/', auth_views.PasswordChangeView.as_view(success_url='/account/profile')),
    path('account/mainpage', views.main_page_view),
    path('passenger/createride', views.CreateRideView.as_view()),
    path('riderequestlist/', views.RideListView.as_view()),
    path('myriderequestlist/', views.MyRideListView.as_view()),
    path('riderequestlist/<int:pk>', views.RideDetailView.as_view()),

    path('passenger/modifyride/<int:rideid>', views.ModifyRideView.as_view()),


    path('driver/drivermsg/<int:driver_id>', views.driverinfoview),

    path('passenger/deleteride/<int:rideid>',views.delete_ride_view),

 
]


