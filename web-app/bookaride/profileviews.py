from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View

from .models import *


def main_page_view(request):
    vehicle = None
    context = {'username': request.user.username}
    try:
        vehicle = Vehicle.objects.get(driver_id=request.user.id)

    except:
        pass

    if vehicle != None:
        context['vehicle'] = vehicle

    return render(request, 'account/mainpage.html', context)


class MyRegisterAsDriverView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'driver/register.html')

    def post(self, request, *args, **kwargs):
        type = request.POST['type']
        license_plate_number = request.POST['license_plate_number']
        max_number_passengers = request.POST['max_number_passengers']
        others = request.POST.get('others', '')

        driver_id = request.user.id

        vehicle = Vehicle.objects.create(driver_id=driver_id, type=type, license_plate_number=license_plate_number, \
                                         max_number_passengers=max_number_passengers, others=others)
        vehicle.save()

        return redirect('/account/mainpage')


class ModifyVehicleView(View):
    def get(self, request, *args, **kwargs):
        context = {'username': request.user.username}

        try:
            vehicle = Vehicle.objects.get(driver_id=request.user.id)
            context['vehicle'] = vehicle
        except:
            pass
        return render(request, 'account/modifyvehicle.html', context)

    def post(self, request, *args, **kwargs):

        type = request.POST.get('type', '')
        license_plate_number = request.POST.get('license_plate_number', '')
        max_number_passengers = request.POST.get('max_number_passengers', '')
        others = request.POST.get('others', '')

        vehicle = Vehicle.objects.all().filter(driver_id=request.user.id)

        if vehicle.count() != 0:

            vehicle = vehicle[0]

            try:
                if type != '':
                    vehicle.type = type

                if license_plate_number != '':
                    vehicle.license_plate_number = license_plate_number

                if max_number_passengers != '':
                    vehicle.max_number_passengers = int(max_number_passengers)

                if others != '':
                    vehicle.others = others
            except:
                pass

            vehicle.save()

        return redirect('/account/profile')


