from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
import json

from models import User, Machine, Ownership
from database import db_session

views = Blueprint('views', __name__)

globalConstants = {
    "title": "Wake on LAN"
}

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

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.admin:
        users = User.query.all()
        return render_template('users.html', users=users, globalConstants=globalConstants)
    else:
        return redirect(url_for('views.index'))

@views.route('/edit', methods=['GET','POST','PUT', 'DELETE'])
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