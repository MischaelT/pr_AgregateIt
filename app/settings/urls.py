from app.currency.views import hello_world

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),

    # currency
    path('hello-world/', hello_world)
]
