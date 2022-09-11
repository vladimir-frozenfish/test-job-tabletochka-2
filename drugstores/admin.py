from django.contrib import admin

from .models import (
    Drugstore,
    Geo,
    Location,
    Schedule,
    ScheduleDrugstore
)


class DrugstoreAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore_id',
        'geo',
        'created_at',
        'updated_at',
        'phone',
        'schedule_representation'
    )
    list_display_links = ('drugstore_id', )


class GeoAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore',
        'address',
        'city_id',
        'city_name',
        'region_id',
        'region_name'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'geo',
        'geo',
        'lat',
        'lon'
    )


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'day',
        'day_name'
    )


class ScheduleDrugstoreAdmin(admin.ModelAdmin):
    list_display = (
        'drugstore',
        'schedule',
        'start',
        'end'
    )


admin.site.register(Drugstore, DrugstoreAdmin)
admin.site.register(Geo, GeoAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleDrugstore, ScheduleDrugstoreAdmin)
