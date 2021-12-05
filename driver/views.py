import json

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Driver
from .serializers import DriverSerializer, DriverSerializerPost
from .services import DriverService
from django.db.models.query import QuerySet


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    basename = "driver"
    serializer_class = DriverSerializer
    serializer_action_classes = {
        'create': DriverSerializerPost,
    }

    def list(self, request):
        date_greater = request.query_params.get('created_at__gte', None)
        date_less = request.query_params.get('created_at__lte', None)
        query = DriverService.filter_by_creation(self.queryset, date_greater, date_less)
        if isinstance(query,QuerySet):
            return Response(self.serializer_class(query, many=True).data)
        return Response(query, status=400)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(DriverViewSet, self).get_serializer_class()

