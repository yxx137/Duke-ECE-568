from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Vehicle(models.Model):
    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=20)
    license_plate_number = models.CharField(max_length=50)
    max_number_passengers = models.IntegerField(default=0)
    others = models.CharField(max_length=300, null=True)

class Request(models.Model):
    owner_info = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    vehicle_info = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        null=True
    )
    vehicle_type = models.CharField(max_length = 20, null=True)
    destination_address = models.CharField(max_length=200)
    driver_id = models.CharField(max_length = 20, null=True)
    arrival_data_time = models.DateTimeField()
    number_passengers = models.IntegerField()
    is_shared = models.BooleanField()
    completed_status = models.IntegerField()
    number_passengers_total = models.IntegerField(default=0)
    Other = models.CharField(max_length=300, null=True)

class ShareList(models.Model):
    sharer_info = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
    )
    number_passengers = models.IntegerField(default=1)