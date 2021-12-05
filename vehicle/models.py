from django.db import models
from django import utils
from driver.models import Driver


class Vehicle(models.Model):
    driver_id = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    make = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    plate_number = models.CharField(max_length=10, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(null=False, blank=False, default=utils.timezone.now)
    updated_at = models.DateTimeField(null=True)
