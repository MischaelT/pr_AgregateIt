from accounts.views import MyProfileView

from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
]
