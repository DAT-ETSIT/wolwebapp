#!/bin/bash

if [ "$EUID" -ne 0 ] 
	then echo "Para poder realizar la instalación, debes ejecutar este script como root."
	exit
fi

if [ $# -ne 2 ]
	then echo "El número de parámetros especificados no es correcto, deben incluirse la dirección y el puerto de escucha. Ejemplo: 'sudo ./install.sh hostname.example.com 8080'"
	exit
fi

path="$(pwd -P | sed -r 's/\//\\\//g')"

echo "Comprobando las dependencias necesarias."
apt update

for check in ethtool python3 python3-pip
    do
        result=`dpkg-query -s $check 2>&1`
        if [[ "$result" == *"is not installed"* ]]; then
            apt-get -y install $check
        fi
    done

pip3 install -r ./requirements.txt

echo "Configurando servicio"

sed -e "s/path/$path/g; s/hostname/$1/g; s/portNumber/$2/g" ./wolsimpleserverExample.service > /etc/systemd/system/wolsimpleserver.service

echo "Iniciando servicio"
sudo systemctl enable wolsimpleserver.service
sudo systemctl start wolsimpleserver.service

echo "Instalación completada"