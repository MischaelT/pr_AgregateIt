import uuid

from accounts.models import User
from accounts.tasks import activate_email

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from django.urls.base import reverse

from settings.settings import DOMAIN, HTTP_SCHEMA


class SignUpCrispyForm(forms.ModelForm):
    """
        Form for signing up

    Args:
        forms (Form): ModelForm
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',
        )

    # Для специфичной валидации можно переопределить этот метод
    def clean(self):

        cleaned_data = super().clean()

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError('Password is not the same')

        return cleaned_data

    def save(self, commit=True):  # Если коммит = фолс, то объект создется, но не уходит в базу данных.

        instance = super().save(commit=False)

        instance.is_active = False
        instance.username = str(uuid.uuid4())
        instance.set_password(self.cleaned_data['password1'])

        activation_path = reverse('accounts:activate-user', args=[instance.username])

        # activate_email.delay(
        #     f"{HTTP_SCHEMA}//{DOMAIN}{activation_path}",
        #     instance.email
        # )
        activate_email(
            f"{HTTP_SCHEMA}//{DOMAIN}{activation_path}",
            instance.email
        )

        if commit:
            instance.save()

        return instance
