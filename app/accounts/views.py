from accounts.forms import SignUpCrispyForm
from accounts.models import User

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import RedirectView


class MyProfileView(LoginRequiredMixin, UpdateView):
    # queryset = User.objects.all()
    fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'avatar',
    )
    success_url = reverse_lazy('accounts:my-profile')
    template_name = 'my_profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserSignUpView(CreateView):
    model = User
    template_name = 'sign-up.html'
    success_url = reverse_lazy('index')
    form_class = SignUpCrispyForm

    def form_valid(self, form):
        messages.info(self.request, 'Thank for registration. Please check your email')
        return super().form_valid(form)


class ActivateView(RedirectView):

    pattern_name = 'index'

    # Если нет переопределить этот метод, то он будет пытаться срендерить страницу с параметром юзернейм, которого нет
    def get_redirect_url(self, *args, **kwargs):

        username = kwargs.pop('username')
        user = get_object_or_404(User, username=username, is_active=False)

        user.is_active = True

        user.save(update_fields=('is_active', ))

        messages.info(self.request, 'Your Account is activated!')

        return super().get_redirect_url(*args, **kwargs)
