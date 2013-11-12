# Create your views here.
from django.views.generic import DetailView, View
from polls.models import Map
from annoying.decorators import JsonResponse


class MapFeaturesMixin(object):
    """
    Provides different features for maps
    """
    def chunks(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    def mapquest_geocode(self, map_geo, locations):
        """batch geocoding 100 pieces at time"""
        mapquest_errors = []
        for objects in self.chunks(locations, 100):
            enc = urllib.urlencode({"locations": objects})
            try:
                resp = urllib2.urlopen("http://open.mapquestapi.com/geocoding/v1/batch", "key={0}&json={{{1}}}".format(settings.MAPQUEST_API_KEY, enc))
                resp_json = json.loads(resp.read())
                if resp_json['info']['statuscode'] != 400:
                    for location in resp_json["results"]:
                        if location["locations"]:
                            result = location["locations"][0]
                            marker, created = Marker.objects.get_or_create(id=location.get("providedLocation").get("id"))
                            marker.geometry = "POINT({0} {1})".format(result["latLng"]["lng"], result["latLng"]["lat"])
                            marker.title = location.get("providedLocation").get("title")
                            marker.short_address = (", ").join([result["street"], result["adminArea4"], result["adminArea3"]])
                            marker.map_geo = map_geo
                            marker.save()
                        else:
                            mapquest_errors.append(location)
                else:
                    mapquest_errors.extend(objects)
            except:
                mapquest_errors.extend(objects)
        return mapquest_errors

    def google_geocode(self, locations, map_geo=None):
        google_errors = []
        for location in locations:
            success = False
            attempts = 0
            if isinstance(location, Marker):
                enc = urllib.urlencode({"address": location.short_address})
            else:
                enc = urllib.urlencode({"address": location["street"]})
            while success is not True and attempts < 3:
                url = "http://maps.googleapis.com/maps/api/geocode/json?{0}&sensor=false".format(enc)
                resp = urllib2.urlopen(url)
                attempts += 1
                if resp.getcode() == 200:
                    resp_json = json.loads(resp.read())
                    if resp_json["status"] == "OK":
                        try:
                            result = resp_json["results"][0]
                            point = result["geometry"]["location"]
                            short_address = result["formatted_address"]
                            if isinstance(location, Marker):
                                marker = location
                            else:
                                marker, created = Marker.objects.get_or_create(id=location.get('id'))
                            marker.title = location["title"]
                            marker.map_geo = map_geo
                            marker.geometry = "POINT({0} {1})".format(point["lng"], point["lat"])
                            marker.short_address = short_address
                            marker.save()
                        except Exception as e:
                            google_errors.append(dict(item=location, message=e.message))
                    elif resp_json["status"] == "OVER_QUERY_LIMIT":
                            #to get rid of Google request limit per second
                            time.sleep(5)
                            continue
                    else:
                        google_errors.append(dict(item=location, message="Google Maps response is {0}".format(resp_json["status"])))
                else:
                    google_errors.append(dict(item=location, message="Google Maps is not reachable."))
                success = True
            if attempts == 3:
                google_errors.append(dict(item=location, message="Daily limit has been reached."))
        return google_errors

    def create_custom_markers(self, locations, map_geo):
        """when coordinates are provided no need to geocode"""
        errors = []
        for location in locations:
            if len(location["coordinates"]) != 2:
                errors.append(dict(item=location, message=u"Missed coordinates field value."))
                continue
            try:
                latitude = float(location["coordinates"][0])
                longitude = float(location["coordinates"][1])
            except TypeError:
                location["coordinates"] = (", ").join(location["coordinates"])
                errors.append(dict(item=location, message=u"Wrong coordinates field value type."))
                continue
            if not -180 < longitude < 180 or not -90 < latitude < 90:
                location["coordinates"] = (", ").join(location["coordinates"])
                errors.append(dict(item=location, message=u"Longtitude values must be between -180 and 180, Latitude between -90 and 90."))
                continue
            try:
                marker, created = Marker.objects.get_or_create(id=location.get('id'))
                marker.geometry = "POINT({0} {1})".format(longitude, latitude)
                marker.title = location["title"]
                marker.short_address = location["street"]
                marker.map_geo = map_geo
                marker.save()
            except Exception as e:
                errors.append(dict(item=location, message=e))
        return errors

    def success(self, map_geo, error_points=None, custom=False):
        """
        returns both geocoded markers and those with errors
        """
        points = [{"title": x.title,
                   "lat": x.geometry.y,
                   "lng": x.geometry.x,
                   "address": x.short_address} for x in Marker.objects.filter(map_geo=map_geo)]
        resp_dict = dict(status="success",
                         message=u"Your data was successfully loaded.",
                         waypoints=points,
                         map_geo=map_geo.id)
        if error_points:
            marker_form = render_to_string("maps/marker-form.html", dict(error_points=error_points,
                                                                         map_geo=map_geo,
                                                                         custom=custom))
            resp_dict.update(dict(message=u"Oops! We were unable to geocode {0} locations on your list. Please, make sure the following information is correct and we'll try again".format(len(error_points)),
                                  marker_form=marker_form))
        return JsonResponse(resp_dict)



class MapDetailView(DetailView):

    #context_object_name = "publisher"
    model = Map

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MapDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['book_list'] = Book.objects.all()
        return context

class FilterPointsView(View):
    def post(self, request, *args, **kwargs):
        try:
            #point_object = fromstr("POINT{0}".format(request.POST.get("point")), srid=4326)
            color=request.POST.get("color")
            map_geo = Map.objects.get(id=request.POST.get("map"))
            markers = [{"title": x.title, "lat": x.geometry.y, "lng": x.geometry.x, "address": x.address, "color": x.color} for x in map_geo.place_set.filter(color=int(color))]
        except Exception as e:
            return JsonResponse(dict(error=e.message, success=False))
        return JsonResponse(dict(markers=markers, success=True))