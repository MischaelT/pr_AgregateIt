from currency.models import Rate

from django.forms import DateInput

import django_filters


class RateFilter(django_filters.FilterSet):

    """
        Filter for rates
    """

    created_gte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created',
        lookup_expr='date__gte',  # Формируется вот по такому шаблону: created__date__gte -
    )

    created_lte = django_filters.DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        field_name='created',
        lookup_expr='date__lte',  # created__date__lte
    )

    class Meta:
        model = Rate
        fields = {
            'bid': ('exact', ),
            'ask': ('exact', ),
            'currency_name': ('exact', ),
        }
