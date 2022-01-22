from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User

from bookaride.models import *


def home(request):
    return HttpResponse("hello")

def oauth_login(request):
    return render(request, 'oauth/login.html')

def oauth_logout(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/index')


@csrf_exempt
def authorize(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        # return HttpResponseRedirect('/account/profile')
        return redirect('/account/profile')

    else:
        # Return an 'invalid login' error message.
        return render(request, 'oauth/login.html', {'errormsg':'login failure'})


@login_required(login_url='/oauth/login/')
def profile(request):
    print(request.user.id)
    vehicle = Vehicle.objects.get(driver_id = request.user.id)
    print(vehicle)
    context = {'username' : request.user.username,'vehicle':vehicle }
    return render(request, 'account/profile.html', context)

def index(request):
    return render(request, 'oauth/index.html')


class MyRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'oauth/register.html')

    def post(self, request, *args, **kwargs):
        
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username, email,password)
        user.save()

        return render(request, 'account/profile.html', {'username':username})


class MyRegisterAsDerverView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'driver/register.html')

    def post(self, request, *args, **kwargs):


        type = request.POST['type']
        license_plate_number = request.POST['license_plate_number']
        max_number_passengers = request.POST['max_number_passengers'] 
        others = request.POST['others']

        driver_id = request.user.id
        
        vehicle = Vehicle.objects.create(driver_id=driver_id,type=type, license_plate_number=license_plate_number,\
        max_number_passengers=max_number_passengers,others=others)
        vehicle.save()

        return render(request, 'account/profile.html', {'vehicle':vehicle})