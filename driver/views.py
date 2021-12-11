from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Driver
from .serializers import DriverSerializer, DriverSerializerCreate, DriverSerializerUpdate, DriverSerializerPartialUpdate
from .services import DriverService
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .filters import CreatedFilter


class DriverViewSet(ModelViewSet):
    """
    Driver View
    """
    queryset = Driver.objects.all()
    basename = "driver"
    filter_class = CreatedFilter
    serializer_class = DriverSerializer
    serializer_action_classes = {
        'create': DriverSerializerCreate,
        'update': DriverSerializerUpdate,
        'partial_update': DriverSerializerPartialUpdate
    }

    def update(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        try:
            driver = DriverService.driver_update(pk, first_name, last_name)
        except ObjectDoesNotExist:
            raise NotFound("Driver not found.")
        return Response(self.get_serializer_class()(driver).data)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        try:
            driver = DriverService.driver_partial_update(pk, first_name, last_name)
        except ObjectDoesNotExist:
            raise NotFound("Driver not found.")
        return Response(self.get_serializer_class()(driver).data)

    def get_serializer_class(self):
        """
        This function choose correct class Serializer for method.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(DriverViewSet, self).get_serializer_class()
