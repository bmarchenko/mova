$(document).ready(function() {
$('.address-search-form').submit(function(e) {

    var point = null;
    var form = $(this);
    $.ajax({
        url: "/search-points",
        type: "post",
        dataType: "json",
        data: form.serialize(),
        success: function(data){
            if (data.success==true){
                var markers = data.markers
                if (markers != false){
                    var mapmarkers = initialize($('#map-'+form.find('.map').val()), markers);
                    var result_list = ''
                    for (var i = 0; i < markers.length-1; i++) {
                        result_list = result_list+'<li class="search-result-item"><p><a id="'+i+'" href="#">'+markers[i].title+'<span>'+markers[i].distance+' mi</span><br>'+markers[i].address+'</a></p></li>'
                    }

//                    form.next().find('ul').html(result_list);
//                    form.next().find('.page_navigation').empty();
//                    form.next().pajinate({
//                        items_per_page : 10,
//                        num_page_links_to_display : 3,
//                        nav_label_first : '',
//                        nav_label_last : '',
//                        abort_on_small_lists: true
//                    });
//                    form.next().find('li a').click(function(){
//                        google.maps.event.trigger(mapmarkers[$(this).attr('id')], 'click');
//                        return false
//                    })
                } else {
                    form.prev().find('div').html("<p>Sorry, we can't find any results that match your search.</p>").parent().show();
                }
            }
        },
        error:function(){
            alert("failure");
        }
    });
//            var color = form.find('.color').val()
//            $.post("/search-points", form.serialize())
//            .done(function(data) {
//                console.log(data)
//                function myfunc(li){google.maps.event.trigger(li, 'click')}
//                if (data.success==true){
//                    var markers = data.markers
//                    if (markers != false){
//                        markers.push({"lat": point.lat(), "lng": point.lng(), "address": '', 'title': results[0].formatted_address, 'special': true, 'radius': radius});
//                        var mapmarkers = initialize($('#map-'+form.find('.map').val()), markers);
//                        var result_list = ''
//                        for (var i = 0; i < markers.length-1; i++) {
//                            result_list = result_list+'<li class="search-result-item"><p><a id="'+i+'" href="#">'+markers[i].title+'<span>'+markers[i].distance+' mi</span><br>'+markers[i].address+'</a></p></li>'
//                        }
//
//                        form.next().find('ul').html(result_list);
//                        form.next().find('.page_navigation').empty();
//                        form.next().pajinate({
//                            items_per_page : 10,
//                            num_page_links_to_display : 3,
//                            nav_label_first : '',
//                            nav_label_last : '',
//                            abort_on_small_lists: true
//                        });
//                        form.next().find('li a').click(function(){
//                            google.maps.event.trigger(mapmarkers[$(this).attr('id')], 'click');
//                            return false
//                        })
//                    } else {
//                        form.prev().find('div').html("<p>Sorry, we can't find any results that match your search.</p>").parent().show();
//                    }
//                } else {
//                    form.prev().find('div').html("<p>Server Error.</p>").parent().show();
//                }
//            });
    return false
});

$('.color').change(function(){
    console.log('sbm')
    var form = $(this).parents('form');
    form.submit()
});

$('.message a').click(function(){
    $(this).parent().hide();
    return false;
})
})