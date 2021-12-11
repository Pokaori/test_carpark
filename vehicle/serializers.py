from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Vehicle
from .services import VehicleService
from driver.models import Driver


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleSerializerCreate(serializers.ModelSerializer):
    def validate_plate_number(self, plate_number):
        plate_number = str(plate_number).strip()
        try:
            return VehicleService.plate_number_validate(plate_number)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def create(self, validated_data):
        try:
            return VehicleService.vehicle_create(**validated_data)
        except ValueError as e:
            raise serializers.ValidationError(e)

    class Meta:
        model = Vehicle
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True}}
        validators = []


class VehicleSerializerUpdate(serializers.ModelSerializer):
    def validate_plate_number(self, plate_number):
        plate_number = str(plate_number).strip()
        try:
            return VehicleService.plate_number_validate(plate_number)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    class Meta:
        model = Vehicle
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True},
                        'driver_id': {"read_only": True}, }
        validators = []


class VehicleSerializerPartialUpdate(serializers.ModelSerializer):
    def validate_plate_number(self, plate_number):
        plate_number = str(plate_number).strip()
        try:
            return VehicleService.plate_number_validate(plate_number)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    class Meta:
        model = Vehicle
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True},
                        'driver_id': {"read_only": True}, 'make': {"required": False}, 'model': {"required": False},
                        'plate_number': {"required": False}}
        validators = []


class VehicleSerializerSetDriver(serializers.ModelSerializer):
    driver_id = serializers.IntegerField(required=True, allow_null=True)
    def validate_driver_id(self, driver_id):
        if driver_id:
            try:
                Driver.objects.get(pk=driver_id)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("Driver not found.")
        return driver_id

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ['make', 'model', 'plate_number', 'created_at', 'updated_at']

