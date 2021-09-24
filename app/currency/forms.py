from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from currency.models import Rate, Source

from django import forms


class RateCrispyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Rate
        fields = (
            'ask',
            'bid',
            'source',
            'currency_name',
        )


class SourceCrispyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Source
        fields = (
            'name',
            'source_url',
            'logo',
        )
