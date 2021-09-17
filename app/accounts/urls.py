from django.urls import path
from accounts.views import MyProfileView, UserSignUpView, ActivateView
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),

    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),

    path('activate/<uuid:username>/', ActivateView.as_view(), name='activate-user'),

]
