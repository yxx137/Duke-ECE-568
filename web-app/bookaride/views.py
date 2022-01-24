from traceback import print_tb
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import DetailView 
from django.shortcuts import get_object_or_404

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
        return redirect('/account/mainpage')

    else:
        # Return an 'invalid login' error message.
        return render(request, 'oauth/login.html', {'errormsg':'login failure'})


@login_required(login_url='/oauth/login/')
def profile(request):

    vehicle = None
    context = {'username' : request.user.username}
    try:
        vehicle = Vehicle.objects.get(driver_id = request.user.id)
        
    except:
        pass

    if vehicle != None :
        context['vehicle']=vehicle
        
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

        return redirect('/account/profile')


class ModifyVehicleView(View):
    def get(self, request, *args, **kwargs):
        context = {'username' : request.user.username }

        try:
            vehicle = Vehicle.objects.get(driver_id = request.user.id)
            context['vehicle']=vehicle
        except:
            pass
        return render(request, 'account/modifyvehicle.html',context)

    def post(self, request, *args, **kwargs):

        type = request.POST.get('type','')
        license_plate_number = request.POST.get('license_plate_number','')
        max_number_passengers = request.POST.get('max_number_passengers','') 
        others = request.POST.get('others','')


        vehicle = Vehicle.objects.all().filter(driver_id = request.user.id)
       
      
        if vehicle.count() != 0:

            vehicle = vehicle[0]

            try:
                if type != '':
                    vehicle.type = type

                if license_plate_number != '':
                    vehicle.license_plate_number = license_plate_number

                if max_number_passengers != '' :
                    vehicle.max_number_passengers = int(max_number_passengers)

                if others != '':
                    vehicle.others = others
            except:
                pass
            
            vehicle.save()

        return redirect('/account/profile')




def main_page_view(request):
    vehicle = None
    context = {'username' : request.user.username}
    try:
        vehicle = Vehicle.objects.get(driver_id = request.user.id)
        
    except:
        pass

    if vehicle != None :
        context['vehicle']=vehicle
        
    return render(request, 'account/mainpage.html', context)


class CreateRideView(View):
    def get(self, request, *args, **kwargs):
        context = {'username' : request.user.username }
        return render(request, 'passenger/createride.html',context)

    def post(self, request, *args, **kwargs):


        vehicle_type = request.POST.get('vehicle_type','')
        destination_address = request.POST.get('destination_address','')
        arrival_data_time = request.POST.get('arrival_data_time','')
        number_passengers = request.POST.get('number_passengers','')
        is_shared = request.POST.get('is_shared','')
        completed_status = 0
        Other = request.POST.get('Other','')

        drive_reuqest = Request.objects.create(vehicle_type=vehicle_type, destination_address=destination_address, \
            arrival_data_time=arrival_data_time, number_passengers=number_passengers, is_shared=is_shared, completed_status=completed_status,\
                Other=Other, owner_info_id = self.request.user.id)


        drive_reuqest.save()
        return redirect('myriderequestlist/')


class RideListView(ListView):
    model = Request
    context_object_name = 'ride_request_list'
    template_name = 'passenger/ridereuqestlist.html'
    # queryset = Request.objects.all().filter(owner_info_id= self.request.user.id)



    def get_context_data(self, **kwargs):
        context = super(RideListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context

    def get_queryset(self):
        return Request.objects.all()



class MyRideListView(ListView):
    model = Request
    context_object_name = 'ride_request_list'
    template_name = 'passenger/ridereuqestlist.html'
    # queryset = Request.objects.all().filter(owner_info_id= self.request.user.id)



    def get_context_data(self, **kwargs):
        context = super(MyRideListView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['modify'] = 'true'
        return context

    def get_queryset(self):
        return Request.objects.all().filter(owner_info_id= self.request.user.id)


class RideDetailView(DetailView):
    model = Request
    context_object_name = 'ride'
    template_name = 'passenger/riderequestdetail.html'

    def book_detail_view(request, primary_key):
        try:
            riderequest = Request.objects.get(pk=primary_key)
        except Request.DoesNotExist:
            raise Http404('Ride does not exist')

        return render(request, '', context={'ride': riderequest})

    
    
# 还没写完
class ModifyRideView(View):
    def get(self, request, *args, **kwargs):
        context = {'username' : request.user.username }

        ride = Request.objects.get(pk = kwargs['rideid'])

        context['ride'] = ride
        return render(request, 'passenger/modifyride.html',context)

    def post(self, request, *args, **kwargs):

        ride = Request.objects.get(pk = kwargs['rideid'])
        destination_address = request.POST.get('destination_address','')
        arrival_data_time = request.POST.get('arrival_data_time','')
        number_passengers = request.POST.get('number_passengers','')
        is_shared = request.POST.get('is_shared','')
        Other = request.POST.get('Other','')

        
        if destination_address != '':
            ride.destination_address = destination_address
        if arrival_data_time != '':
            ride.arrival_data_time = arrival_data_time
        if number_passengers != '':
            ride.number_passengers = number_passengers
        if is_shared != '':
            ride.is_shared = is_shared
        if Other != '':
            ride.Other = Other

        ride.save()
        return redirect('/myriderequestlist/')


def modifyrideview(request,driver_id):

    context = {'username' : request.user.username }
    if request.method == 'POST':
        # Your code for POST
        pass
    else:
        
        context['driver_id'] = driver_id
      
    
    return render(request, 'passenger/modifyride.html',context )



def driverinfoview(request,driver_id):

    vehicle = Vehicle.objects.get(driver_id = driver_id)
    context = {'vehicle':vehicle}

    user = User.objects.get(id = driver_id)
    context['drivername'] = user.username
    context['driveremail'] = user.email
    context['username'] = request.user.username

    return render(request, 'driver/drivermsg.html',context)
    