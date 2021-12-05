from rest_framework import serializers
from datetime import datetime
from .models import Driver

class DriverService:
    @staticmethod
    def filter_by_creation(query, date_greater=None, date_less=None):
        try:
            format_greater=None
            format_less=None
            if date_greater:
                format_greater = datetime.strptime(str(date_greater), "%d-%m-%Y")
                query= query.filter(created_at__gte=format_greater)
            if date_less:
                format_less = datetime.strptime(str(date_less), "%d-%m-%Y")
                query = query.filter(created_at__lte=format_less)
            if format_greater and format_less and format_less < format_greater:
                if format_less < format_greater:
                    return {"error": "created_at__lte can`t be less than created_at__gte"}
        except ValueError:
            return {"error": "Date format is incorrect"}
        return query

    @staticmethod
    def name_validate(first_name):
        if not first_name.isalpha():
            raise ValueError('Name has only letters')
        if not first_name[0].isupper():
            raise ValueError('Name should be capitalized')
        return first_name
    @staticmethod
    def last_name_validate(last_name):
        last_name = str(last_name).strip()
        last_names = last_name.split('-')
        for name in last_names:
            DriverService.name_validate(name)
        return last_name


    @staticmethod
    def driver_create(first_name, last_name, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can't be earlier, then created_at")
        if not created_at:
            created_at=datetime.now()
        driver = Driver.objects.create(first_name=first_name, last_name=last_name,
                                       created_at=created_at, updated_at=updated_at)
        return driver
