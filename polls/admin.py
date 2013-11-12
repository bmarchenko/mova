from django.contrib.gis import admin
from django.contrib import messages
from polls.views import MapFeaturesMixin
from polls import models
from django.contrib.admin.options import ModelAdmin
from django.contrib.gis import admin


def geocode_action(modeladmin, request, queryset):
    google_errors = MapFeaturesMixin.google_geocode(queryset)
    if google_errors:
        messages.error(request, "Oops! We were unable to geocode {0} locations on your list. Please, make sure marker is correct".format(len(google_errors)))
    else:
        messages.success(request, "Successfully geocoded {0} objects".format(len(queryset)))
geocode_action.short_description = u"Geocode"

class MarkerAdmin(ModelAdmin):
    list_display = ("title", "map_geo", "geocoded")
    list_filter = ("geocoded", "map_geo")
    exclude = ("geocoded", )
    actions = [geocode_action]


admin.site.register(models.Region)
admin.site.register(models.Place, admin.OSMGeoAdmin)
admin.site.register(models.Poll)
admin.site.register(models.Profile)
admin.site.register(models.Map)
