from currency.views import get_contact_us
from currency.views import hello_world

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', hello_world),
    path('get-contactUs/', get_contact_us),

]
