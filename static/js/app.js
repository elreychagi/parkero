var list_parkings = [];

function show_parking(id){
    var estacionamiento = localStorage.getItem(id);
    if(estacionamiento != null){
        var json_est = JSON.parse(estacionamiento);
        var datos_meta = function(){
            var meta = '';
            if(json_est.motos){
                meta += '<li>Motos</li>';
            }
            if(json_est.camiones){
                meta += '<li>Camiones</li>';
            }
            if(!json_est.sin_techo){
                meta += '<li>Techado</li>';
            }else{
                meta += '<li>Sin techo</li>';
            }
            return meta;
        }

        var set_points = function(data_puntos){
            $('.wrapper-points').html('');
            var puntos = '';
            for(var i=1; i < 6; i++){
                if(data_puntos < i){
                    puntos += '<i class="icon-star-empty point" data-point="' + i + '"></i>';
                }else{
                    puntos += '<i class="icon-star point" data-point="' + i + '"></i>';
                }
            }
            $('.wrapper-points').html(puntos);
        }
        var datos_html = '<div class="modal-header">' +
                             '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>' +
                             '<h3 id="myModalLabel">' + json_est.nombre + '</h3>' +
                         '</div>' +
                         '<div class="modal-body">' +
                             '<span><strong>Puntaje</strong></span>  ' +
                             '<span class="wrapper-points"></span><br>' +
                             '<strong>Descripcion:</strong>' +
                             '<p>' + json_est.descripcion + '</p>' +
                             '<ul>' +
                                 datos_meta() +
                             '</ul>' +
                         '</div>' +
                         '<div class="modal-footer">' +
                             '<div class="wrapper-comment-form">' +
                                 '<form class="navbar-form pull-left" style="width: 100%;">' +
                                     '<strong>¿Tienes algún comentario?</strong><br>' +
                                     '<textarea class="area_comment" style="width: 98%;"></textarea>' +
                                     '<small>140 caractéres máximo<small><br>' +
                                     '<button type="submit" class="btn_send_comment">Enviar</button>' +
                                 '</form>' +
                             '</div>' +
                             '<div class="wrapper-comments">' +
                                 '<div class="commets-box">' +
                                     '<p>laksjdfl akdjfdsak lfjds</p>' +
                                     '<a class="control-comment">cerrar</a>' +
                                 '</div>' +
            '<div class="commets-box">' +
            '<p>laksjdfl akdjfdsak lfjds</p>' +
            '<a class="control-comment">cerrar</a>' +
            '</div>' +
            '<div class="commets-box">' +
            '<p>laksjdfl akdjfdsak lfjds</p>' +
            '<a class="control-comment">cerrar</a>' +
            '</div>' +
                             '</div>' +
                         '</div>';
        $('#wrapper_detalles').html(datos_html);
        set_points(json_est.puntos);
        $('#wrapper_detalles').modal('show');

        $('.area_comment').keyup(function(){
            if($('.area_comment').val().length > 140) {
                $('.area_comment').val($('.area_comment').val().substring(0, 140))
            }
        });

        $('.point').click(function(){
            $this = $(this);
            $.post('/app/set_points/' + json_est.id + '/' + $this.data('point') + '/',
                {'csrfmiddlewaretoken' : csr},
                function(data){
                    if(data.success){
                        set_points(data.puntos);
                    }
                });
        });

        $('.navbar-form').click(function(e){
            $this = $(this);
            if($this.find('textarea').val() == '')return false;
            e.preventDefault();
            $.post('/comentarios/set_comment/' + json_est.id + '/',
                {'csrfmiddlewaretoken' : csr, 'contenido' : $this.find('textarea').val()},
                function(data){
                    if(data.success){
                        alert(data.comentario);
                    }
                });
        })
    }
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
                    map: map
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
                                localStorage.setItem(v.id, JSON.stringify(v));
                                console.log(v.id, v);

                                google.maps.event.addListener(marker, "click", function() {
                                    show_parking(v.id);
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
    localStorage.setItem('a', 'b');
    alert(localStorage.getItem('a'));
    $('#map_canvas').height($('#map_canvas').height() - 60);

    var useragent = navigator.userAgent;

    if (useragent.indexOf('iPhone') == -1 && useragent.indexOf('Android') == -1 ) {
        $('#map_canvasd').css({'width':'600px'});
    }

    get_parkings();
    window.onorientationchange = function(){}
});
