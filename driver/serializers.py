from rest_framework import serializers
from .models import Driver
from .services import DriverService
from datetime import datetime


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverSerializerPost(serializers.ModelSerializer):
    def validate_first_name(self, first_name):
        first_name = str(first_name).strip()
        try:
            return DriverService.name_validate(first_name)
        except ValueError as e:
            raise serializers.ValidationError("First "+str(e))

    def validate_last_name(self, last_name):
        # last_name = str(last_name).strip()
        # last_names = last_name.split('-')
        try:
            # for name in last_names:
            #     DriverService.name_validate(name)
            # return last_name
            return  DriverService.last_name_validate(last_name)
        except ValueError as e:
            raise serializers.ValidationError("Every Last "+str(e))

    # def validate(self, data):
    #     created_at= data.get('created_at', None)
    #     updated_at = data.get('updated_at', None)
    #     if created_at and updated_at and updated_at < created_at:
    #         raise serializers.ValidationError("created_at can't be bigger, than updated_at")
    #     return data
    def create(self, validated_data):
        try:
            return  DriverService.driver_create(**validated_data)
        except ValueError as e:
            serializers.ValidationError(str(e))

    class Meta:
        model = Driver
        fields = "__all__"
        extra_kwargs = {'created_at': {"read_only": True}, 'updated_at': {"read_only": True}}
        validators = []
