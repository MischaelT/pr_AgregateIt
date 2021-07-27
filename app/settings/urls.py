from currency.views import get_contact_us, index, rate_list

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('contactUs/', get_contact_us),
    path('rate/list/', rate_list),

]
