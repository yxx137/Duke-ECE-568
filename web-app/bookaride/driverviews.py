
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import *

class DriverSearchView(View):
    def get(self, request, *args, **kwargs):
        userId = request.user.id
        userVehicle = Vehicle.objects.get(driver=userId)
        def addAction(data):
            c = data.__dict__
            c['edit'] = '/driver/ride/' + str(data.id)
            return c
        openRequests = Request.objects.filter(completed_status=0, vehicle_type=userVehicle.type, number_passengers__lte=userVehicle.max_number_passengers)
        openRequestsNull = Request.objects.filter(completed_status=0, vehicle_type__isnull=True, number_passengers__lte=userVehicle.max_number_passengers)
        openRequestsWithAction = map(addAction, list(openRequests) + list(openRequestsNull))
        confirmedRequests = Request.objects.filter(completed_status=1, vehicle_info=userVehicle.id)
        return render(request, 'driver/search.html', {'openRequests': openRequestsWithAction, 'confirmedRequests': confirmedRequests})


class DriverRideView(View):
    def get(self, request, ride_id):
        userId = request.user.id
        userVehicle = Vehicle.objects.get(driver=userId)
        ride = Request.objects.get(id=ride_id)
        return render(request, 'driver/ride.html', {'ride': ride})

@csrf_exempt
def DriverConfirmRide(request):
    ride_id = request.POST['ride_id']
    ride = Request.objects.get(id=ride_id)
    ride.completed_status = 1
    ride.save()
    owner = User.objects.get(id=ride.owner_info_id)
    return redirect('/driver/ride/' + ride_id + '/')
"""
    send_mail(
        'Ride confirmed',
        'Your ride with id ' + ride_id + ' is confirmed',
        'from@example.com',
        [owner.email],
        fail_silently=False,
    )
"""


@csrf_exempt
def DriverCompeteRide(request):
    ride_id = request.POST['ride_id']
    ride = Request.objects.get(id=ride_id)
    ride.completed_status = 2
    ride.save()

    return redirect('/driver/ride/'+ride_id+'/')