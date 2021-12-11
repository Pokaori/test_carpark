from rest_framework import serializers
from .models import Driver
from .services import DriverService


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverSerializerCreate(serializers.ModelSerializer):
    def validate_first_name(self, first_name):
        first_name = str(first_name).strip()
        try:
            return DriverService.name_validate(first_name)
        except ValueError as e:
            raise serializers.ValidationError("First " + str(e))

    def validate_last_name(self, last_name):
        try:
            last_name = str(last_name).strip()
            return DriverService.last_name_validate(last_name)
        except ValueError as e:
            raise serializers.ValidationError("Every Last " + str(e))

    def create(self, validated_data):
        try:
            return DriverService.driver_create(**validated_data)
        except ValueError as e:
            serializers.ValidationError(str(e))

    class Meta:
        model = Driver
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True}}
        validators = []


class DriverSerializerUpdate(serializers.ModelSerializer):
    def validate_first_name(self, first_name):
        first_name = str(first_name).strip()
        try:
            return DriverService.name_validate(first_name)
        except ValueError as e:
            raise serializers.ValidationError("First " + str(e))

    def validate_last_name(self, last_name):
        try:
            return DriverService.last_name_validate(last_name)
        except ValueError as e:
            raise serializers.ValidationError("Every Last " + str(e))

    class Meta:
        model = Driver
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True}}
        validators = []


class DriverSerializerPartialUpdate(serializers.ModelSerializer):
    def validate_first_name(self, first_name):
        first_name = str(first_name).strip()
        try:
            return DriverService.name_validate(first_name)
        except ValueError as e:
            raise serializers.ValidationError("First " + str(e))

    def validate_last_name(self, last_name):
        try:
            return DriverService.last_name_validate(last_name)
        except ValueError as e:
            raise serializers.ValidationError("Every Last " + str(e))

    class Meta:
        model = Driver
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True},
                        'first_name': {"required": False}, 'last_name': {"required": False}}
        validators = []
