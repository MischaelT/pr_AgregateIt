from currency.views import (
    create_rate,
    create_source,
    delete_rate,
    delete_source,
    get_contact_us,
    get_rate_details,
    get_source_details,
    index,
    rate_list,
    source_list,
    update_rate,
    update_source,
)

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('contactUs/', get_contact_us),
    path('rate/list/', rate_list),
    path('rate/create/', create_rate),
    path('rate/details/<int:rate_id>/', get_rate_details),
    path('rate/update/<int:rate_id>/', update_rate),
    path('rate/delete/<int:rate_id>/', delete_rate),
    path('source/list/', source_list),
    path('source/create/', create_source),
    path('source/details/<int:source_id>/', get_source_details),
    path('source/update/<int:source_id>/', update_source),
    path('source/delete/<int:source_id>/', delete_source),
]
