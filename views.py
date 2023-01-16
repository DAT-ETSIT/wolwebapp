from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from subprocess import run, PIPE

from models import User, Machine, Ownership
import data.serverConfig as config

views = Blueprint('views', __name__)

def canUpdate():
    # a = run(['git status'], shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # print(a)
    result = run('git status --branch --porcelain | grep -o behind', shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    return result.stdout.replace('\n','')

@views.route('/', methods=['GET'])
@login_required
def index():
    if request.method == 'GET':
        if current_user.activated:
            machines = []
            if hasattr(current_user, 'admin'):
                owner = Ownership.query.filter_by(user_id = current_user.id).all()
                for machine in owner:
                    machines.append(Machine.query.get(machine.machine_id))
            return render_template('index.html', TITLE=config.TITLE, machines=machines, isAdmin=current_user.admin, canUpdate=canUpdate())
        else:
            return render_template('changePassword.html')


@views.route('/machines', methods=['GET'])
@login_required
def machines():
    if current_user.admin:
        if request.method == 'GET':
            machines = Machine.query.all()
            return render_template('machines.html', machines=machines, TITLE=config.TITLE, isAdmin=current_user.admin)  
    else:
        abort(403)


@views.route('/users', methods=['GET'])
@login_required
def users():
    if current_user.admin:
        
        # Recupera los datos de todos los usuarios.
        if request.method == "GET":

            users = User.query.all()
            return render_template('users.html', users=users, TITLE=config.TITLE, isAdmin=current_user.admin, currentUserId=current_user.id)

    else:
        abort(403)


@views.route('/users/<int:user_id>/machines', methods=['GET'])
@login_required
def user_machines(user_id):
    if current_user.admin:
        if request.method == 'GET':
            machines = Machine.query.all()
            ownerships = Ownership.query.filter_by(user_id=user_id).all()
            owned_machines = []
            for machine in ownerships:
                owned_machines.append(machine.id)
            return render_template('ownership.html', machines=machines, owned_machines=owned_machines, TITLE=config.TITLE, isAdmin=current_user.admin)

    else:
        abort(403)