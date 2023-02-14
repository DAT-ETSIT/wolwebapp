# Wolsimpleserver

Wolsimlpeserver es un aplicación que posibilita el encendido remoto de ordenadores en remoto, monitorizar el estado de los mismos y la gestión de usuarios y sus permisos, todo ello desde un interfaz web. 
<!-- El objetivo es desplegar el servicio en un equipo de bajo consumo que estará conectado para así reducir las horas que están los ordenadores encendidos. -->

## Instalación del servicio

Para configurar la instalación del servicio tan solo es necesario descargar el fichero `install.sh` y ejecutarlo en una shell de Linux, siguiendo estos pasos:

```bash
wget https://raw.githubusercontent.com/pablofl01/wolsimpleserver/main/install.sh
chmod +x install.sh
sudo ./install.sh
```

A continuación se detalla el funcionamiento del mismo:

Comprueba que estén instaladas las dependencias necesarias y en caso de que haya alguna que no, la instala. Las dependencias necesarias son: `git python3 python3-pip python3-venv openssl wakeonlan`.

Una vez instaladas las dependencias, clona el repositorio [wolsimpleserver](https://github.com/Pablofl01/wolsimpleserver) y cambia el directorio de trabajo al generado con la clonación.

En caso de no proporcionar un certificado propio (ver apartado [Argumentos](#argumentos)), el terminal solicitará algunos parámetros para generarlo de forma automática.

Con el certificado ya introducido o generado, se crea un entorno virtual de python para la aplicación en el que se instalan las librerías necesarias para la misma. Estas se encuentran en el fichero `requirements.txt`.

Entre los comentarios que van apareciendo en el terminal el script solicita un nombre "identificativo del servidor", este nombre es el que aparecerá en las cabeceras de los correos que se envían de forma automática. También hay que introducir manualmente el correo y la contraseña del primer administrador de la aplicación (esta contraseña se podrá modificar más adelante en la propia aplicación).

Finalmente se configura el envío de mensajes por correo electrónico y se levanta el servicio. Este servicio se utiliza para el envío de las credenciales temporales para el alta o modificación de usuarios sin que el administrador pueda conocerlas.

### Argumentos 

Los argumentos que pueden utilizarse a la hora de instalar 

```bash
-h   Mostrar ayuda
-b   BIND_ADDRESS - Dirección de la interfaz de reden la que escuchará el servidor (por defecto 0.0.0.0).
-p   PORT - Puerto empleado por la aplicación. Si se inicia en modo 'standalone' se emplean 80 y 443 por defecto, si se configura para emplear junto con un proxy inverso, se emplea el 3000.
-w   PARENT_PATH - Directorio donde se instalará la aplicación (por     
                   defecto /srv).
-m   SERVER_MODE - STANDALONE o REVERSE_PROXY.
-c   CERT_PATH - Ruta del certificado SSL.
-k   KEY_PATH - Clave del certificado SSL.
```
