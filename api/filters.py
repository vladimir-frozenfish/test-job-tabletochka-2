from django_filters.rest_framework import CharFilter, FilterSet, filters

from drugstores.models import Drugstore


class DrugstoreFilter(FilterSet):
    city = CharFilter(field_name='geo__city_name')
    region = CharFilter(field_name='geo__region_name')

    class Meta:
        model = Drugstore
        fields = ['city', 'region']

