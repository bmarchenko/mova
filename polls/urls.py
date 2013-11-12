from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib.gis import admin
from polls.views import MapDetailView
from polls.views import FilterPointsView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', TemplateView.as_view(template_name='polls/homepage.html'), name="home"),
    url(r"^(?P<slug>\w+)$", MapDetailView.as_view(), name="map"),

    #url(r'^map/$', MapView.as_view(), name='map'),
    #url(r'^mova/', include('mova.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r"^search-points", FilterPointsView.as_view(), name="search_points"),

)
