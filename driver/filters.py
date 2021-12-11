import django_filters
from datetime import datetime
from rest_framework.exceptions import ValidationError


class CreatedFilter(django_filters.FilterSet):
    def filter_created__gte(self, query, name, value):
        try:
            if value:
                value = datetime.strptime(str(value), "%d-%m-%Y")
                query = query.filter(created_at__gte=value)
        except ValueError as e:
            raise ValidationError({"created_at__gte": str(e)})
        return query

    def filter_created__lte(self, query, name, value):
        try:
            if value:
                value = datetime.strptime(str(value), "%d-%m-%Y")
                query = query.filter(created_at__lte=value)
        except ValueError as e:
            raise ValidationError({"created_at__lte": str(e)})
        return query

    created_at__gte = django_filters.CharFilter(field_name='created_at', lookup_expr='gte',
                                                method='filter_created__gte')
    created_at__lte = django_filters.CharFilter(field_name='created_at', lookup_expr='lte',
                                                method='filter_created__lte')
