from django_filters import rest_framework as filters

from currency.models import Rate


class RateFilter(filters.FilterSet):

    class Meta:
        model = Rate
        fields = {
            'bid': ('lt', 'lte', 'gt', 'gte', 'exact'),
            'ask': ('lt', 'lte', 'gt', 'gte', 'exact'),
            # 'type': ('in', ),
            # 'created': ('date', 'lte', 'gte'),
        }
        