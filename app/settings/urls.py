from currency.views import (
    ContactUsListView,
    IndexView,
    RateCreateView,
    RateDeleteView,
    RateDetailView,
    RateListView,
    RateUpdateView,
    SourceCreateView,
    SourceDeleteView,
    SourceDetailView,
    SourceListView,
    SourceUpdateView,

)
import debug_toolbar

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view()),
    path('contactUs/', ContactUsListView.as_view()),
    path('rate/list/', RateListView.as_view()),
    path('rate/create/', RateCreateView.as_view()),
    path('rate/details/<int:pk>/', RateDetailView.as_view()),
    path('rate/update/<int:pk>/', RateUpdateView.as_view()),
    path('rate/delete/<int:pk>/', RateDeleteView.as_view()),
    path('source/list/', SourceListView.as_view()),
    path('source/create/', SourceCreateView.as_view()),
    path('source/details/<int:pk>/', SourceDetailView.as_view()),
    path('source/update/<int:pk>/', SourceUpdateView.as_view()),
    path('source/delete/<int:pk>/', SourceDeleteView.as_view()),

    path('__debug__/', include(debug_toolbar.urls)),
]
