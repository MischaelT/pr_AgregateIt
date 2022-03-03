from currency.models import ContactUs, Rate

from django_filters import rest_framework as filters


class RateFilter(filters.FilterSet):

    """
        Filter class for rates api page
    """

    class Meta:
        model = Rate
        fields = {
            'bid': ('lt', 'lte', 'gt', 'gte', 'exact'),
            'ask': ('lt', 'lte', 'gt', 'gte', 'exact'),
        }


class ContactUsFilter(filters.FilterSet):

    """
        Filter class for contacts us lists api page
    """

    class Meta:
        model = ContactUs
        fields = {
            'created': ('lt', 'lte', 'gt', 'gte', 'exact'),
            # 'subject': ('lt', 'lte', 'gt', 'gte', 'exact'),
        }
