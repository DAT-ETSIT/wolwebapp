#!/bin/bash

if [ $# -ne 1 ]
	then echo "No se ha indicado nombre de host. Ejemplo: 'sudo ./install.sh hostname.example.com'"
	exit
fi

if [ "$EUID" -ne 0 ] 
	then echo "Para poder realizar la instalación, debes ejecutar este script como root."
	exit
fi

echo "Instalando dependencias necesarias"
pip3 install -r ./requirements.txt

echo "Configurando servicio"
sed "s/hostname/$1/g" ./wolsimpleserverExample.service > /etc/systemd/system/wolsimpleserver.service

echo "Iniciando servicio"
sudo systemctl start wolsimpleserver.service

echo "Instalación completada"