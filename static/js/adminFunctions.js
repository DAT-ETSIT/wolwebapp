function checkUpdates(currentVersion){
    $.ajax({
        method: 'GET',
        url: 'https://api.github.com/repos/DAT-ETSIT/wolwebapp/commits/main'
    }).done(function (response) {
        if ( currentVersion !== response['sha']) {
            $('#updateAlert').html("Hay una <a href='https://github.com/DAT-ETSIT/wolwebapp'>nueva versión</a> de la aplicación disponible");
        }
    })
};