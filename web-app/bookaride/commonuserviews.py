from django.http.response import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView

from .models import *


class CreateRideView(View):
    def get(self, request, *args, **kwargs):
        context = {'username' : request.user.username }
        return render(request, 'passenger/createride.html' ,context)

    def post(self, request, *args, **kwargs):


        vehicle_type = request.POST.get('vehicle_type' ,'')
        destination_address = request.POST.get('destination_address' ,'')
        arrival_data_time = request.POST.get('arrival_data_time' ,'')
        number_passengers = request.POST.get('number_passengers' ,'')
        is_shared = request.POST.get('is_shared' ,'')
        completed_status = 0
        Other = request.POST.get('Other' ,'')

        drive_reuqest = Request.objects.create(vehicle_type=vehicle_type, destination_address=destination_address, \
                                               arrival_data_time=arrival_data_time, number_passengers=number_passengers, is_shared=is_shared, completed_status=completed_status, \
                                               Other=Other, owner_info_id = self.request.user.id)


        drive_reuqest.save()
        return redirect('/myriderequestlist/')


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



class MyRideListView(View):
 


    def get(self, request, *args, **kwargs):
        context = {}
        context['username'] = self.request.user.username
        context['modify'] = 'true'
        context['ride_request_list'] = Request.objects.all().filter(owner_info_id= self.request.user.id)


        context['share'] = 'true'
        share_ride_request_list = []
        context['share_ride_request_list'] = share_ride_request_list

        sharequeryset = ShareList.objects.all().filter(sharer_info = self.request.user.id)

        request_ids = []
        for share in sharequeryset:
            request_ids.append(share.request_id)

        for id in request_ids:
            share_ride_request_list.append(Request.objects.get(id = id))
        
        return render(request, 'passenger/ridereuqestlist.html', context)




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
        return render(request, 'passenger/modifyride.html' ,context)

    def post(self, request, *args, **kwargs):

        ride = Request.objects.get(pk = kwargs['rideid'])
        destination_address = request.POST.get('destination_address' ,'')
        arrival_data_time = request.POST.get('arrival_data_time' ,'')
        number_passengers = request.POST.get('number_passengers' ,'')
        is_shared = request.POST.get('is_shared' ,'')
        Other = request.POST.get('Other' ,'')


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


def modifyrideview(request ,driver_id):

    context = {'username' : request.user.username }
    if request.method == 'POST':
        # Your code for POST
        pass
    else:

        context['driver_id'] = driver_id


    return render(request, 'passenger/modifyride.html' ,context )



def driverinfoview(request ,driver_id):

    vehicle = Vehicle.objects.get(driver_id = driver_id)
    context = {'vehicle' :vehicle}

    user = User.objects.get(id = driver_id)
    context['drivername'] = user.username
    context['driveremail'] = user.email
    context['username'] = request.user.username

    return render(request, 'driver/drivermsg.html' ,context)

def delete_ride_view(request ,rideid):


    ride = Request.objects.get(id = rideid)
    ride.delete()

    return redirect('/myriderequestlist/')

