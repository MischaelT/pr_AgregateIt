from api.v1 import views

from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

router = DefaultRouter()

router.register(r'rates', views.RateViewSet, basename='rate')
router.register(r'sources', views.SourceViewSet, basename='source')
router.register(r'contact-us', views.ContactUsViewSet, basename='contact-us')

urlpatterns = [
    path('choices/', views.RateChoicesView.as_view(), name='currency_choices'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns.extend(router.urls)
