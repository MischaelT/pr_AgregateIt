from rest_framework.routers import DefaultRouter
from api.v1 import views

app_name = 'api'

router = DefaultRouter()

router.register(r'rates', views.RateViewSet, basename='rate')   

urlpatterns = [
]

urlpatterns.extend(router.urls)