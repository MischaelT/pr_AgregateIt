from currency.models import Rate

from import_export import resources


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'source',
            'currency_name',
        )
