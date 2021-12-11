
from datetime import datetime
from .models import Driver


class DriverService:
    """
    Driver Service to separate Business Logic.
    """

    @staticmethod
    def name_validate(first_name):
        if not first_name.isalpha():
            raise ValueError('Name has only letters')
        first_name=first_name.capitalize()
        return first_name

    @staticmethod
    def last_name_validate(last_name):
        last_names = last_name.split('-')
        names=[]
        for name in last_names:
            names.append(DriverService.name_validate(name))
        return "-".join(names)

    @staticmethod
    def driver_create(first_name, last_name, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        if not created_at:
            created_at = datetime.now()
        driver=Driver.objects.create(first_name=first_name, last_name=last_name,
                                     created_at=created_at, updated_at=updated_at)
        return driver


    @staticmethod
    def driver_update(pk, first_name, last_name, created_at=None, updated_at=None):
        driver = Driver.objects.get(pk=pk)
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        driver.first_name = first_name
        driver.last_name = last_name
        if created_at:
            driver.created_at = created_at
        if updated_at:
            driver.updated_at = updated_at
        else:
            driver.updated_at = datetime.now()
        driver.save()
        return driver

    @staticmethod
    def driver_partial_update(pk, first_name=None, last_name=None, created_at=None, updated_at=None):
        driver = Driver.objects.get(pk=pk)
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        if first_name:
            driver.first_name = first_name
        if last_name:
            driver.last_name = last_name
        if created_at:
            driver.created_at = created_at
        if updated_at:
            driver.updated_at = updated_at
        else:
            driver.updated_at = datetime.now()
        driver.save()
        return driver
