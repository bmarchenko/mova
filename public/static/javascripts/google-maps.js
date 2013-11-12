String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
    return typeof args[number] != 'undefined'
    ? args[number]
    : match
    ;
    });
};

function initialize(container, points){
    var markers = [];
    var circle = null
    var infoWindow = new google.maps.InfoWindow({});
    var mapProp = {
        center:new google.maps.LatLng(0, 0),
        zoom:5,
        mapTypeId:google.maps.MapTypeId.ROADMAP
        };
    var map = new google.maps.Map(container[0],mapProp);
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < points.length; i++) {
        var title = points[i].title
        var position = new google.maps.LatLng(points[i].lat, points[i].lng)
        if (points[i].special != true){
            if (points[i].color == 1) {
                var icon = 'http://maps.gstatic.com/mapfiles/ms2/micons/red.png'
            }
            else if (points[i].color == 2) {
                var icon = 'http://maps.gstatic.com/mapfiles/ms2/micons/yellow.png'
            }
            else {
                var icon = 'http://maps.gstatic.com/mapfiles/ms2/micons/green.png'

            }

        } else {
            var icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
            var radius = points[i].radius
            var zoom
            if (radius < 200){
                circle = new google.maps.Circle({
                    map: map,
                    radius: points[i].radius*1609.34,    // metres
                    fillColor: 'blue'
                });
                if (radius == 20) {
                    zoom = 9
                }
                else if (radius == 10) {
                    zoom = 10
                }
                else {
                    zoom = 11
                }
                map.setZoom(zoom);
            }
        }
        var marker = new google.maps.Marker({
            position: position,
            title: title,
            icon: icon
        });

        markers.push(marker);
        marker.set('location', points[i]);
        bounds.extend(position);
        marker.setMap(map);

        if (circle != null){
            circle.bindTo('center', marker, 'position');
            map.panTo(position);
        }

        google.maps.event.addListener(marker, 'click', function() {
            var location = this.get('location');
            var tem = '<div class="av-areaInfo">'+location.title+'<br>Адреса: '+location.address+'</div>'
            var cardTemplate = $(tem).html();
            infoWindow.setContent(cardTemplate);
            infoWindow.open(map, this);
        });

    }

    container.css("width", "100%").css("height", "98%")
    if (circle == null){
        map.fitBounds(bounds);
    }

    return markers

}

