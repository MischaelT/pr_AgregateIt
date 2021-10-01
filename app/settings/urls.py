import debug_toolbar

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Aggregator API",
      default_version='v1',
      description="Bank rates",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Непонятно к какому приложению относится индекс-страница, поэтому счаще всего делают таким образом
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('currency/', include('currency.urls')),

    path('accounts/', include('accounts.urls')),

    path('api/', include('api.v1.urls')),

    path('__debug__/', include(debug_toolbar.urls)),

    url('accounts/', include('django.contrib.auth.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
