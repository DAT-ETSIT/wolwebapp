function checkUpdates(currentVersion){
    $.ajax({
        method: 'GET',
        url: 'https://api.github.com/repos/pablofl01/wolsimpleserver/commits/Caronte'
    }).done(function (response) {
        if ( currentVersion !== response['sha']) {
            $('#updateAlert').html("Hay una <a href='https://github.com/DAT-ETSIT/wolwebapp'>nueva versión</a> de la aplicación disponible");
        }
    })
};