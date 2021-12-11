from rest_framework.exceptions import NotFound, APIException
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from .models import Vehicle
from .serializers import VehicleSerializer, VehicleSerializerCreate, VehicleSerializerUpdate, \
    VehicleSerializerPartialUpdate, VehicleSerializerSetDriver
from .services import VehicleService
from django.core.exceptions import ObjectDoesNotExist
from .filters import DriversFilter


class VehicleViewSet(ModelViewSet):
    """
    Vehicle View
    """
    queryset = Vehicle.objects.all()
    basename = "vehicle"
    serializer_class = VehicleSerializer
    serializer_action_classes = {
        'create': VehicleSerializerCreate,
        'update': VehicleSerializerUpdate,
        'partial_update': VehicleSerializerPartialUpdate
    }
    filter_class = DriversFilter

    def update(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        make = validated_data.get('make')
        model = validated_data.get('model')
        plate_number = validated_data.get('plate_number')
        try:
            vehicle = VehicleService.vehicle_update(pk, make, model, plate_number)
        except ObjectDoesNotExist:
            raise NotFound("Vehicle not found.")
        return Response(self.get_serializer_class()(vehicle).data)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        make = validated_data.get('make')
        model = validated_data.get('model')
        plate_number = validated_data.get('plate_number')
        try:
            vehicle = VehicleService.vehicle_partial_update(pk, make, model, plate_number)
        except ObjectDoesNotExist:
            raise NotFound("Vehicle not found.")
        return Response(self.get_serializer_class()(vehicle).data)

    def get_serializer_class(self):
        """
        This function choose correct class Serializer for method.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(VehicleViewSet, self).get_serializer_class()

    # def get_serializer(self, *args, **kwargs):
    #     try:
    #         return self.serializer_action_classes[self.action]
    #     except (KeyError, AttributeError):
    #         return super(VehicleViewSet, self).get_serializer_class()


class VehicleSetDriverViewSet(GenericViewSet):
    """
    Vehicle Set Driver View.
    As we have unusual endpoint(.../set_driver/<vehicle_id>/ instead of .../vehicle/set_driver/<vehicle_id>/)
    we had to create a separate ViewSet.
    """
    queryset = Vehicle.objects.all()
    basename = "set_driver"
    serializer_class = VehicleSerializerSetDriver

    @action(detail=True, methods=['post'], name='Set Driver.')
    def set_driver(self, request, pk=None):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        driver_id = validated_data.get('driver_id')
        try:
            vehicle = VehicleService.set_driver(pk, driver_id)
        except ObjectDoesNotExist:
            raise NotFound("Vehicle not found.")
        except ValueError as e:
            exc = APIException(detail=e, code=status.HTTP_409_CONFLICT)
            exc.status_code = 409
            raise exc
        return Response(self.serializer_class(vehicle).data)
