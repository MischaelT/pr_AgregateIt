from api.v1.filters import ContactUsFilter, RateFilter
from api.v1.paginators import ContactUsPagination, RatePagination, SourcePagination
from api.v1.serializer import ContactUsSerializer, RateSerializer, SourceSerializer
from api.v1.throttles import AnonUserRateThrottle

from currency import model_choices as choices
from currency.models import ContactUs, Rate, Source

from django_filters import rest_framework as filters

from rest_framework import filters as rest_framework_filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response


class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all().select_related('source')
    serializer_class = RateSerializer
    pagination_class = RatePagination
    filterset_class = RateFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ['id', 'created', 'ask', 'bid']
    throttle_classes = [AnonUserRateThrottle]
    search_fields = ['currency_name', 'source__name']


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    pagination_class = SourcePagination


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    pagination_class = ContactUsPagination
    filterset_class = ContactUsFilter
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
        rest_framework_filters.SearchFilter,
    )
    ordering_fields = ['id', 'created']
    throttle_classes = [AnonUserRateThrottle]
    search_fields = ['subject', 'email_from']


class SourceChoicesView(generics.GenericAPIView):
    def get(self, request):
        return Response(
            {'source_names': choices.SOURCE_TYPES}
        )


class RateChoicesView(generics.GenericAPIView):
    def get(self, request):
        return Response(
            {'rate_names': choices.RATE_TYPES}
        )
