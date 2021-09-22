import debug_toolbar

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Непонятно к какому приложению относится индекс-страница, поэтому счаще всего делают таким образом
    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('currency/', include('currency.urls')),

    path('accounts/', include('accounts.urls')),

    path('__debug__/', include(debug_toolbar.urls)),

    url('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]

urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
