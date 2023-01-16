#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

update() {
    read -r -p "Hay una nueva versión disponible, ¿actualizar? (S/N) " response
    if [[ "$response" == "S" || "$response" == "s" ]]; then   
        git pull
        systemctl restart wolsimpleserver.service
    else
        echo "Se ha cancelado la operación"
        exit()
    fi
}

git fetch
upcheck=`git status --branch --porcelain | grep -o behind`
if [ "$upcheck" == "behind" ]; then 
    update
else
    echo "La aplicación ya se encuentra en su última versión."
fi