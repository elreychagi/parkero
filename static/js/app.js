$(document).ready(function(){
    $.get(
        '/users/list_parkings/',
        {'lat' : '10.498400682444014',
        'long' : '-66.9158148765564'},
        function(data){

        }
    )
});
