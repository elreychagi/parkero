$(document).ready(function(){
    var $lat = false;
    var $long = false;

    var useragent = navigator.userAgent;
    if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
        $('#map_canvas').css({'width':'100%', 'height':'100%'});
    } else {
        $('#map_canvas').css({'width':'600px', 'height':'800px'});
    }

    navigator.geolocation.getCurrentPosition(function (position) {
        $lat = position.coords.latitude;
        $long = position.coords.longitude;
        var point = new google.maps.LatLng($lat, $long);
        var mapOptions = {
            center: point,
            zoom: 16,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
        var marker = new google.maps.Marker({
            position: point,
            map: map,
            title: 'Hello World!'
        });

        $.get(
            '/geo/list_parkings/',
            {'lat' : $lat,
            'long' : $long},
            function(data){
                $.each(data.parkings, function(i, v){
                    var marker = new google.maps.Marker({
                        position: new google.maps.LatLng(v.latitude, v.longitude),
                        map: map,
                        icon: new google.maps.MarkerImage("/static/img/taxi.png"),
                        title: 'Hello World!'
                    });
                });
            }
        );
    },
        function(){alert('error');},
        { enableHighAccuracy:true }
    );
});


function initialize() {
    var myLatlng = new google.maps.LatLng(-25.363882,131.044922);
    var mapOptions = {
        zoom: 4,
        center: myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    var map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);

    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'Hello World!'
    });
}
