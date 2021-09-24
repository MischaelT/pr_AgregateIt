from currency.models import Rate, Source

from django import forms


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'currency_name',
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'name',
            'source_url',
        )
