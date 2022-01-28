from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import *




class SharerSearchView(View):
    def get(self, request, *args, **kwargs):
        userId = request.user.id

        return render(request, 'sharer/search.html', {'openRequests': [], 'confirmedRequests': [], 'type': 'from get'})

    def post(self, request, *args, **kwargs):
        destination = request.POST.get('destination', '')
        arrival_time_earliest = request.POST.get('arrival_time_earliest', '')
        arrival_time_latest = request.POST.get('arrival_time_latest', '')
        passenger_number = request.POST.get('passenger_number', '')

        userId = request.user.id
        userVehicle = Vehicle.objects.get(driver=userId)

        #if len(destination)==0:
        #    openRequests = Request.objects.filter(completed_status=0, is_shared=True)
        if len(arrival_time_earliest)==0 or len(arrival_time_latest)==0 :
            openRequests = Request.objects.filter(completed_status=0, is_shared = True,
                                                  destination_address = destination)
        else:
            openRequests = Request.objects.filter(completed_status=0, is_shared = True,
                                                  arrival_data_time__gt=arrival_time_earliest,
                                                  arrival_data_time__lt=arrival_time_latest,
                                                  destination_address = destination)
        return render(request, 'sharer/search.html', {'openRequests': openRequests, 'confirmedRequests': [], 'type': 'from post'})
