from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
import json
import random
import string

from models import User, Machine, Ownership
from database import db_session

views = Blueprint('views', __name__)

globalConstants = {
    "title": "Wake on LAN"
}

def randomPass():
    password = ""
    for i in range(6):
        password += random.choice(string.ascii_letters)
    return password

@views.route('/', methods=['GET'])
@login_required
def index():
    if request.method == 'GET':
        print("GET")
        machines = []
        if hasattr(current_user, 'admin'):
            owner = Ownership.query.filter_by(user_id = current_user.id).all()
            for machine in owner:
                machines.append(Machine.query.get(machine.machine_id))
        return render_template('machines.html', globalConstants=globalConstants, machines=machines)

@views.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def users():
    if current_user.admin:
        
        # Recupera los datos de todos los usuarios.
        if request.method == "GET":

            users = User.query.all()
            return render_template('users.html', users=users, globalConstants=globalConstants)

        # Actualiza los datos del usuario especificado.
        elif request.method == 'POST':
            user = User.query.filter_by(id=request.json['id']).first()
            if user:
                try:
                    user.admin = True if request.json['admin'] == 0 else False
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

        # Guarda el nuevo usuario especificado en la base de datos.
        elif request.method == 'PUT':

            email = request.json['email']
            password = randomPass()
            newUser = User(email, password)
            try:
                db_session.add(newUser)
                db_session.commit()
                user = User.query.filter_by(email=request.json['email']).first()
                response = {
                    'code': 0,
                    'id': user.id
                }
            except:
                response = {
                    'code': 1,
                    'message': "Error al guardar el usuario en la base de datos."
                }
            finally:
                return response

        # Elimina el usuario especificado.
        elif request.method == 'DELETE':
            user = User.query.filter_by(id=request.json['id']).first()
            if user:
                try:
                    db_session.delete(user)
                    db_session.commit()
                    response = {
                        'code': 0,
                        'id': request.json['id']
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
        return redirect(url_for('views.index'))

@views.route('/users/<int:user_id>', methods=['GET','PUT', 'DELETE'])
@login_required
def owners(user_id):
    if current_user.admin:
        if request.method == 'GET':
            machines = Machine.query.all()
            ownerships = Ownership.query.filter_by(user_id=user_id).all()
            owned_machines = []
            for machine in ownerships:
                owned_machines.append(machine.id)
            return render_template('ownership.html', machines=machines, owned_machines=owned_machines, globalConstants=globalConstants)

        if request.method == 'DELETE':
            try:
                edit_ownership = Ownership.query.filter_by(user_id = user_id, machine_id=request.json["machine_id"]).first()
                if edit_ownership:
                    db_session.delete(edit_ownership)
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

        if request.method == 'PUT':
            try:
                edit_ownership = Ownership(user_id=user_id, machine_id=request.json["machine_id"])
                print(edit_ownership)
                db_session.add(edit_ownership)
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

@views.route('/edit', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def machineEdit():
    if current_user.admin:
        if request.method == 'GET':
            machines = Machine.query.all()
            return render_template('editMachines.html', machines=machines, globalConstants=globalConstants)

        elif request.method == 'POST':

            update_machine = Machine.query.get(request.json['id'])

            name = request.json['name']
            mac = request.json['mac']
            ip = request.json['ip']

            if Machine.query.filter_by(name = name, mac = mac, ip = ip).first():
                return ""

            update_machine.name = name
            update_machine.mac = mac
            update_machine.ip = ip
            db_session.commit()

            return "Guardado"

        elif request.method == 'PUT':

            name = request.json['name']
            mac = request.json['mac']
            ip = request.json['ip']
            new_machine = Machine(name, mac, ip, "7")
            if Machine.query.filter_by(name = name, mac = mac, ip = ip).first():
                return ""
            db_session.add(new_machine)
            db_session.commit()

            return "Guardado"

        elif request.method == 'DELETE':

            db_session.delete(Machine.query.get(request.json['id']))
            db_session.commit()
            
            return "Eliminado"
            
    else:
        return redirect(url_for('views.index'))

@views.route('/getMachine', methods=['POST'])
@login_required
def getMachine():
    if request.method == 'POST':
        machine = Machine.query.filter_by(name = request.json['name'], mac = request.json['mac'], ip = request.json['ip']).first()
        if machine:
            return str(machine.id)
        else:
            return "Error"
