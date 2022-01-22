from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 254, null = True)


class Vehicle(models.Model):
    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length = 20)
    license_plate_number = models.CharField(max_length = 50)
    max_number_passengers = models.IntegerField(default=0)
    others = models.CharField(max_length = 300)


class Request(models.Model):
    owner_info = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    vehicle_info = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )
    vehicle_type = models.CharField(max_length = 20)
    destination_address = models.CharField(max_length = 200)
    arrival_data_time = models.DateTimeField()
    number_passengers = models.IntegerField()
    is_shared = models.BooleanField()
    completed_status = models.IntegerField()
    Other = models.CharField(max_length = 300)


class ShareList(models.Model):
    sharer_info = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
    )