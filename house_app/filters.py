import django_filters

from .models import Property


class PropertyFilter(django_filters.FilterSet):
    # диапазоны «от / до»
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    area_from = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    area_to = django_filters.NumberFilter(field_name='area', lookup_expr='lte')

    land_area_from = django_filters.NumberFilter(field_name='land_area', lookup_expr='gte')
    land_area_to = django_filters.NumberFilter(field_name='land_area', lookup_expr='lte')

    ceiling_from = django_filters.NumberFilter(field_name='ceiling_height', lookup_expr='gte')
    ceiling_to = django_filters.NumberFilter(field_name='ceiling_height', lookup_expr='lte')

    floor_from = django_filters.NumberFilter(field_name='floor', lookup_expr='gte')
    floor_to = django_filters.NumberFilter(field_name='floor', lookup_expr='lte')

    total_floors_from = django_filters.NumberFilter(field_name='total_floors', lookup_expr='gte')
    total_floors_to = django_filters.NumberFilter(field_name='total_floors', lookup_expr='lte')

    class Meta:
        model = Property
        fields = {
            'deal_type': ['exact'],
            'property_type': ['exact'],
            'region': ['iexact'],
            'city': ['iexact'],
            'district': ['iexact'],
            'rooms': ['exact'],
            'condition': ['exact'],
            'house_type': ['exact'],
            'legal_docs': ['exact'],
            'currency': ['exact'],
            'price_type': ['exact'],
            'from_owner': ['exact'],
            'exchange_possible': ['exact'],
            'installment_possible': ['exact'],
            'mortgage_possible': ['exact'],
            'is_urgent': ['exact'],
            'has_cadastre_report': ['exact'],
        }