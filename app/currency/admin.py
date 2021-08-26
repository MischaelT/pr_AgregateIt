from currency.models import ContactUs, Rate, Source
from currency.resource import RateResource

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from rangefilter.filters import DateRangeFilter


class RateAdmin(ImportExportModelAdmin):

    resource_class = RateResource

    list_display = (
        'id',
        'ask',
        'bid',
        'currency_name',
        'source',
        'created',
    )
    list_filter = (
        'currency_name',
        'source',
        ('created', DateRangeFilter),
    )
    search_fields = (
        'currency_name',
        'source',
    )
    readonly_fields = (
        'ask',
        'bid',
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SourceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'source_url',
    )
    list_filter = (
        'name',
        'id',
    )
    search_fields = (
        'name',
    )


class ContactUsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'email_from',
        'subject',
        'message',
        'created',
    )
    list_filter = (
        'id',
        ('created', DateRangeFilter),
    )
    search_fields = (
        'subject',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Rate, RateAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
