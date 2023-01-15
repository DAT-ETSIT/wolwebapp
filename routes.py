from flask import Blueprint, request, redirect, url_for, abort
from flask_login import login_required, current_user
import random
import string

from models import User, Machine, Ownership
from database import db_session
import mail.mail as mail
import data.serverConfig as config

routes = Blueprint('routes', __name__)


def randomPass():
    password = ""
    for i in range(6):
        password += random.choice(string.ascii_letters)
    return password


@routes.route('/machines', methods=['POST', 'PUT'])
@login_required
def machines():
    if current_user.admin:
        if request.method == 'PUT':

            name = request.json['name']
            mac = request.json['mac']
            ip = request.json['ip']
            port = request.json['port']


            if Machine.query.filter_by(name = name, mac = mac, ip = ip, port = port).first():
                response = {
                    'code': 1,
                    'message': "Ya existe una máquina con los mismos datos."
                }

            else:
                try:
                    new_machine = Machine(name, mac, ip, port)
                    db_session.add(new_machine)
                    db_session.commit()

                    machine = Machine.query.filter_by(name = name, mac = mac, ip = ip, port = port).first()
                    response = {
                        'code': 0,
                        'id': machine.id
                    }

                except:
                    response = {
                        'code': 2,
                        'message': "Error al añadir la máquina a la base de datos."
                    }

            return response

        #elif request.method == 'POST':
        #    machine = Machine.query.filter_by(name = request.json['name'], mac = request.json['mac'], ip = request.json['ip']).first()
        #    if machine:
        #        return str(machine.id)
        #    else:
        #        return "Error"
            
    else:
        abort(403)


@routes.route('/machines/<int:machineId>', methods=['POST', 'DELETE'])
@login_required
def machine(machineId):
    if current_user.admin:
        if request.method == 'POST':
            update_machine = Machine.query.get(machineId)

            name = request.json['name']
            mac = request.json['mac']
            ip = request.json['ip']
            port = request.json['port']

            if Machine.query.filter_by(id=machineId).first():
                if not Machine.query.filter_by(name = name, mac = mac, ip = ip, port = port).first():
                    try:
                        update_machine.name = name
                        update_machine.mac = mac
                        update_machine.ip = ip
                        update_machine.port = port
                        db_session.commit()

                        response = {
                            'code': 0
                        }

                    except:
                        response = {
                            'code': 1,
                            'message': "Error al actualizar la máquina en la base de datos."
                        }

                else:
                    response = {
                        'code': 2,
                        'message': "Ya existe una máquina con los mismos datos."
                    }
            
            else:
                response = {
                    'code': 3,
                    'message': "La máquina especificada no existe."
                }

            return response
        
        elif request.method == 'DELETE':
            if Machine.query.filter_by(id=machineId).first():
                try:
                    db_session.delete(Machine.query.get(machineId))
                    db_session.commit()
                    response = {
                            'code': 0
                    }

                except:
                    response = {
                        'code': 1,
                        'message': "Error al eliminar la máquina de la base de datos."
                    }

            else:
                response = {
                    'code': 2,
                    'message': "La máquina especificada no existe."
                }
            
            return response
    else:
        abort(403)
        

@routes.route('/users', methods=['PUT'])
@login_required
def users():
    if current_user.admin:

        # Guarda el nuevo usuario especificado en la base de datos.
        if request.method == 'PUT':

            email = request.json['email']

            if User.query.filter_by(email=request.json['email']).first():
                response = {
                    'code': 3,
                    'message': "Ya existe un usuario con ese email."
                }

                return response

            password = randomPass()
            newUser = User(email, password)
            try:
                db_session.add(newUser)
                db_session.commit()
                user = User.query.filter_by(email=request.json['email']).first()
                mailResult = mail.sendMail(email, f"Nuevas credenciales en {config.SERVER_NAME}", mail.buildMessage('newUser', {'$PASSWORD': password, '$ADMIN_EMAIL': config.ADMIN_EMAIL}))
                if mailResult == 0:
                    response = {
                        'code': 0,
                        'id': user.id
                    }
                elif mailResult == 1:
                    response = {
                    'code': 2,
                    'message': "No se han configurado las credenciales para enviar mensajes de correo."
                }
            except:
                response = {
                    'code': 1,
                    'message': "Error al guardar el usuario en la base de datos."
                }
            return response

    else:
        return redirect(url_for('routes.index'))


@routes.route('/users/<int:userId>', methods=['PATCH', 'POST', 'DELETE'])
@login_required
def user(userId):
    if current_user.admin:

        # Resetea la contraseña del usuario especificado.
        if request.method == 'PATCH':
            user = User.query.filter_by(id=userId).first()
            if user:
                try:
                    password = randomPass()
                    user.password = password
                    db_session.commit()

                    mailResult = mail.sendMail(user.email, f"Reestablecimiento de contraseña en {config.SERVER_NAME}", mail.buildMessage('resetPassword', {'$PASSWORD': password, '$ADMIN_EMAIL': config.ADMIN_EMAIL}))
                    if mailResult == 0:
                        response = {
                            'code': 0
                        }
                    elif mailResult == 1:
                        response = {
                            'code': 3,
                            'message': "No se han configurado las credenciales para enviar mensajes de correo."
                        }

                except:
                    response = {
                        'code': 2,
                        'message': "Error al resetear la contraseña del usuario."
                    }
            else:
                response = {
                        'code': 1,
                        'message': "El usuario especificado no existe."
                    }

            return response

        # Actualiza los datos del usuario especificado.
        elif request.method == 'POST':
            user = User.query.filter_by(id=userId).first()
            if user:
                try:
                    user.password = True if request.json['admin'] == 0 else False
                    db_session.commit()
                    isAdmin = '1' if user.admin else '0'
                    response = {
                        'code': 0,
                        'isAdmin': isAdmin
                    }
                except:
                    response = {
                        'code': 2,
                        'message': "Error al cambiar los permisos del usuario."
                    }
            else:
                response = {
                        'code': 1,
                        'message': "El usuario especificado no existe."
                    }

            return response

        
        # Elimina el usuario especificado.
        elif request.method == 'DELETE':
            user = User.query.filter_by(id=userId).first()
            if user:
                try:
                    db_session.delete(user)
                    db_session.commit()
                    response = {
                        'code': 0,
                        'id': userId
                    }
                except:
                    response = {
                        'code': 2,
                        'message': "Error al buscar el usuario en la base de datos."
                    }
            else:
                response = {
                        'code': 1,
                        'message': "El usuario especificado no existe."
                    }

            return response
    else:
        abort(403)


@routes.route('/users/<int:userId>/machines', methods=['PUT', 'DELETE'])
@login_required
def user_machines(userId):
    if current_user.admin:

        if request.method == 'PUT':
            try:
                new_ownership = Ownership(user_id=userId, machine_id=request.json["machine_id"])
                print(new_ownership)
                db_session.add(new_ownership)
                db_session.commit()
                response = {
                    'code': 0,
                    'isOwned': 1
                }
            except:
                response = {
                    'code': 1,
                    'message': "Error añadiendo propiedad a la máquina {request.json['machine_id']}."
                }
            return response

        elif request.method == 'DELETE':
            try:
                ownership = Ownership.query.filter_by(user_id = userId, machine_id=request.json["machine_id"]).first()
                if ownership:
                    db_session.delete(ownership)
                db_session.commit()
                response = {
                    'code': 0,
                    'isOwned': 0
                }
            except:
                response = {
                    'code': 1,
                    'message': f"Error eliminando la propiedad de la máquina {request.json['machine_id']}."
                }
            return response

    else:
        abort(403)