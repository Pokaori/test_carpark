from datetime import datetime
from .models import Vehicle
from django.db.utils import IntegrityError
from driver.models import Driver


class VehicleService:
    """
    Vehicle Service to separate Business Logic.
    """

    @staticmethod
    def plate_number_validate(plate_number: str):
        plate_number_parts = plate_number.split()
        if len(plate_number_parts) != 3:
            raise ValueError("Plate number should have 3 parts.")
        if len(plate_number_parts[0]) != 2 or not plate_number_parts[0].isalpha():
            raise ValueError("Incorrect first part. It should have format 'AA'.")
        if not plate_number_parts[1].isdigit() or len(plate_number_parts[1]) != 4:
            raise ValueError("Incorrect second part. It should have format '1234'.")
        if len(plate_number_parts[2]) != 2 or not plate_number_parts[2].isalpha():
            raise ValueError("Incorrect third part. It should have format 'OO'.")
        plate_number_parts[0] = plate_number_parts[0].upper()
        plate_number_parts[2] = plate_number_parts[2].upper()
        return " ".join(plate_number_parts)

    @staticmethod
    def vehicle_create(make, model, plate_number, driver_id=None, created_at=None, updated_at=None):
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        if not created_at:
            created_at = datetime.now()
        try:
            if driver_id:
                driver = Driver.objects.get(pk=driver_id)
                vehicle = Vehicle.objects.create(make=make, model=model, plate_number=plate_number, driver_id=driver,
                                                 created_at=created_at, updated_at=updated_at)
            else:
                vehicle = Vehicle.objects.create(make=make, model=model, plate_number=plate_number,
                                                 created_at=created_at, updated_at=updated_at)
        except IntegrityError as e:
            raise ValueError(e)
        return vehicle

    @staticmethod
    def vehicle_update(pk, make, model, plate_number, created_at=None, updated_at=None):
        vehicle = Vehicle.objects.get(pk=pk)
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        vehicle.make = make
        vehicle.model = model
        vehicle.plate_number = plate_number
        if created_at:
            vehicle.created_at = created_at
        if updated_at:
            vehicle.updated_at = updated_at
        else:
            vehicle.updated_at = datetime.now()
        vehicle.save()
        return vehicle

    @staticmethod
    def vehicle_partial_update(pk, make=None, model=None, plate_number=None, created_at=None, updated_at=None):
        vehicle = Vehicle.objects.get(pk=pk)
        if created_at and updated_at and updated_at < created_at:
            raise ValueError("updated_at can`t be less than created_at")
        if make:
            vehicle.make = make
        if model:
            vehicle.model = model
        if plate_number:
            vehicle.plate_number = plate_number
        if created_at:
            vehicle.created_at = created_at
        if updated_at:
            vehicle.updated_at = updated_at
        else:
            vehicle.updated_at = datetime.now()
        vehicle.save()
        return vehicle

    @staticmethod
    def set_driver(pk, driver_id):
        vehicle = Vehicle.objects.all().get(pk=pk)
        if not driver_id:
            vehicle.driver_id = None
        elif vehicle.driver_id is not None:
            raise ValueError("This vehicle already has driver. Please, unset driver first (set null)")
        else:
            vehicle.driver_id = Driver.objects.get(pk=driver_id)
        try:
            vehicle.save()
        except IntegrityError:
            raise ValueError("This driver already has vehicle.")
        return vehicle
