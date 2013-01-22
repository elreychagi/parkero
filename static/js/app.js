var list_parkings = [];

function get_comments(){

}

function get_parkings(recarga){
    navigator.geolocation.getCurrentPosition(function (position) {
            var $lat = position.coords.latitude;
            var $long = position.coords.longitude;

            if(typeof recarga != 'undefined' && localStorage.getItem('position') != null && localStorage.getItem('position') == $lat + $long){
                setTimeout('get_parkings(true)', 30000);
            }else{
                localStorage.setItem('position', $lat + $long);

                var point = new google.maps.LatLng($lat, $long);
                var mapOptions = {
                    center: point,
                    zoom: 16,
                    styles:[
                        { featureType: "road", stylers: [{hue: "#006Eee"}]}
                    ],
                    mapTypeId: google.maps.MapTypeId.ROADMAP
                }
                var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
                var marker = new google.maps.Marker({
                    position: point,
                    map: map,
                    title: 'Hello World!'
                });

                var data = {'lat' : $lat, 'long' : $long}
                if(typeof recarga != 'undefined'){data['recarga'] = true;}

                $.get(
                    '/geo/buscar_estacionmientos/',
                    data,
                    function(data){
                        $.each(data.parkings, function(i, v){
                            if(list_parkings.indexOf(v.latitud + v.longitud) == -1){
                                var marker = new google.maps.Marker({
                                    position: new google.maps.LatLng(v.latitud, v.longitud),
                                    map: map,
                                    icon: new google.maps.MarkerImage("/static/img/taxi.png"),
                                    title:v.name
                                });
                                google.maps.event.addListener(marker, "click", function() {
                                    alert(v.id);
                                });
                            }
                        });
                        google.maps.event.addListener(map, 'center_changed', function() {
                            get_parkings(true);
                        });
                        setTimeout('get_parkings(true)', 30000);
                    }
                );
            }
        },
        function(){alert('Error al obtener posición');},
        { enableHighAccuracy:true }
    );
}

$(document).ready(function(){
    var $lat = false;
    var $long = false;

    $('#map_canvas').height($('#map_canvas').height() - 60);

    var useragent = navigator.userAgent;

    if (useragent.indexOf('iPhone') == -1 && useragent.indexOf('Android') == -1 ) {
        $('#map_canvasd').css({'width':'600px'});
    }

    get_parkings();
    window.onorientationchange = function(){alert('dkj')}
});
