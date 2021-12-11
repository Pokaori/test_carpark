import django_filters

CHOICES = [("yes", "With drivers"), ("no", "Without drivers")]


class DriversFilter(django_filters.FilterSet):
    def filter_drivers(self, queryset, name, value):
        if value == "yes":
            queryset = queryset.filter(driver_id__isnull=False)
        else:
            queryset = queryset.filter(driver_id__isnull=True)
        return queryset
    with_drivers = django_filters.ChoiceFilter(label="Choose option:", method='filter_drivers',
                                               choices=CHOICES)
