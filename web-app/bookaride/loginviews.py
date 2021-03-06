from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

from .models import *


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
        return redirect('/account/mainpage')

    else:
        # Return an 'invalid login' error message.
        return render(request, 'oauth/login.html', {'errormsg': 'login failure'})


@login_required(login_url='/oauth/login/')
def profile(request):
    vehicle = None
    context = {'username': request.user.username}
    try:
        vehicle = Vehicle.objects.get(driver_id=request.user.id)

    except:
        pass

    if vehicle != None:
        context['vehicle'] = vehicle

    return render(request, 'account/profile.html', context)


class MyRegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'oauth/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username, email, password)
        user.save()

        return render(request, 'account/profile.html', {'username': username})
