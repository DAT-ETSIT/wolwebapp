#!/bin/bash

if [ "$EUID" -ne 0 ] 
    then echo "Para poder realizar la configuración, debes ejecutar este script como root."
	exit
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

getData() {
    read -r -p "Introduce la cuenta de correo electrónico desde la que se enviarán los mensajes: " MAIL_USER

    while [ true ]
    do
        read -r -s -p "Introduce la contraseña de la cuenta: " MAIL_PASS
        echo
        read -r -s -p "Confirma la contraseña de la cuenta: " CONFIRM_MAIL_PASS
        echo

        if [[ $MAIL_PASS == $CONFIRM_MAIL_PASS ]];then
            break;
        else
            echo "Las contraseñas no coinciden."
            echo
        fi
    done

    read -r -p "Introduce el nombre que aparecerá en los mensajes enviados: " MAIL_NAME
    read -r -p "Introduce la dirección del servidor SMTP: " MAIL_SERVER
    read -r -p "Introduce el puerto del servidor SMTP: " MAIL_PORT
    echo
}

getData

while [ true ]
do
    echo "------------------"
    echo "Nombre: $MAIL_NAME"
    echo "Usuario: $MAIL_USER"
    echo "Servidor: $MAIL_SERVER"
    echo "Puerto: $MAIL_PORT"
    read -r -p "¿Son correctos estos datos? (S/N) " response
    if [[ "$response" == "S" || "$response" == "s" ]]; then        
		break
    elif [[ "$response" == "N" || "$response" == "n" ]]; then
        getData
    else
        echo "Opción no válida"
        echo ""
    fi
done

sed -e "s/<MAIL_USER>/$MAIL_USER/g; s/<MAIL_NAME>/$MAIL_NAME/g; s/<MAIL_SERVER>/$MAIL_SERVER/g; s/<MAIL_PORT>/$MAIL_PORT/g" -i $SCRIPT_DIR/data/serverConfig.py
$WORKING_PATH/bin/python3 $SCRIPT_DIR/generateSecrets.py