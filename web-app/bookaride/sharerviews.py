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

        filterArgs = {'completed_status':0, 'is_shared':True}
        if len(destination)!=0:
            filterArgs['destination_address'] = destination
        if len(arrival_time_earliest)!=0:
            filterArgs['arrival_data_time__gt'] = arrival_time_earliest

        if len(arrival_time_latest)!=0:
            filterArgs['arrival_data_time__lt'] = arrival_time_latest

        openRequests = Request.objects.filter(**filterArgs)

        openRequests2 = list(map(lambda r: r.__dict__, list(openRequests)))
        firstRequest = openRequests2[0]
        firstRequest['joinShare'] = '/sharer/search/joinsharer/' + str(firstRequest['id'])
        return render(request, 'sharer/search.html', {'openRequests': openRequests2})

class SharerJoin(View):
    def get(self, request, ride_id, **kwargs):
        userId = request.user.id

        return render(request, 'sharer/joinsharer.html', {'ride_id':ride_id})

class ConfirmJoin(View):
    def post(self, request, *args, **kwargs):
        userId = request.user.id
        sharer_number = request.POST.get('number', '')
        ride_id = request.POST.get('ride_id', '')
        sharer_list = ShareList.objects.create(sharer_info_id=userId, request_id = ride_id, number_passengers=sharer_number)
        sharer_list.save()
        return redirect('/account/mainpage')
