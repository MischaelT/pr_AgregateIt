from accounts.views import ActivateView, MyProfileView, UserSignUpView

from django.urls import path

app_name = 'accounts'

urlpatterns = [

    path('my-profile/', MyProfileView.as_view(), name='my-profile'),

    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),

    path('activate/<uuid:username>/', ActivateView.as_view(), name='activate-user'),

]
