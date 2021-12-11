from django.db import models
from datetime import datetime

class Driver(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(null=False,blank=False)
    updated_at = models.DateTimeField(null=True)

    def __int__(self):
        return self.id
