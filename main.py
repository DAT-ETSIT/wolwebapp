from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_required, login_user, LoginManager

import json
import os
from subprocess import call, run, PIPE
from markupsafe import escape

from database import db, init_db, db_session
from models import User, Machine
from auth import auth
from views import views

login_manager = LoginManager()

app = Flask(__name__)

init_db()

users = User.query.all()
if users == []:
    if os.environ.get('ADMIN_MAIL') != None and os.environ.get('ADMIN_PASS') != None:
        newUser = User(email=os.environ.get('ADMIN_MAIL'), password=os.environ.get('ADMIN_PASS'))
        newUser.admin = True
        db_session.add(newUser)
        db_session.commit()
    else:
        print("Deben especificarse las credenciales del administrador inicial mediante las variables de entorno ADMIN_MAIL y ADMIN_PASS.")
        exit(1)

app.secret_key = 'ASHFLIASJF'
app.register_blueprint(auth)
app.register_blueprint(views)
login_manager.login_view = "auth.login"
login_manager.init_app(app)

globalConstants = {
    "title": "Wake on LAN"
}

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

machines = Machine.query.all()

@app.route('/wol/<int:machineId>', methods=['POST'])
@login_required
def wolMachine(machineId):
    if request.method != 'POST':
        return redirect(url_for('index'))
    result = run(['wakeonlan', '-p', machines[machineId]["port"], machines[machineId]["mac"]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if result.stderr != '':
        return '<svg class="iconRed" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512c141.4 0 256-114.6 256-256S397.4 0 256 0S0 114.6 0 256S114.6 512 256 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zm32 224c0 17.7-14.3 32-32 32s-32-14.3-32-32s14.3-32 32-32s32 14.3 32 32z"/></svg>'
    else:
        return '<svg class="iconGreen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M470.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-256 256c-12.5 12.5-32.8 12.5-45.3 0l-128-128c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L192 338.7 425.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/></svg>'

@app.route('/ping/<int:machineId>', methods=['POST', 'GET'])
@login_required
def pingMachine(machineId):
    if request.method != 'POST':
        return redirect(url_for('index'))
    machine = Machine.query.get(int(machineId))
    result = run(['ping', '-c', '5' , machine.ip], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if result.stderr != '':
        return '<svg class="iconRed" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512c141.4 0 256-114.6 256-256S397.4 0 256 0S0 114.6 0 256S114.6 512 256 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zm32 224c0 17.7-14.3 32-32 32s-32-14.3-32-32s14.3-32 32-32s32 14.3 32 32z"/></svg>'
    if '0 received' in result.stdout:
        return '<svg class="iconRedX" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M96 0C78.3 0 64 14.3 64 32v96h64V32c0-17.7-14.3-32-32-32zM288 0c-17.7 0-32 14.3-32 32v96h64V32c0-17.7-14.3-32-32-32zM32 160c-17.7 0-32 14.3-32 32s14.3 32 32 32v32c0 77.4 55 142 128 156.8V480c0 17.7 14.3 32 32 32s32-14.3 32-32V412.8c12.3-2.5 24.1-6.4 35.1-11.5c-2.1-10.8-3.1-21.9-3.1-33.3c0-80.3 53.8-148 127.3-169.2c.5-2.2 .7-4.5 .7-6.8c0-17.7-14.3-32-32-32H32zM432 512c79.5 0 144-64.5 144-144s-64.5-144-144-144s-144 64.5-144 144s64.5 144 144 144zm59.3-180.7L454.6 368l36.7 36.7c6.2 6.2 6.2 16.4 0 22.6s-16.4 6.2-22.6 0L432 390.6l-36.7 36.7c-6.2 6.2-16.4 6.2-22.6 0s-6.2-16.4 0-22.6L409.4 368l-36.7-36.7c-6.2-6.2-6.2-16.4 0-22.6s16.4-6.2 22.6 0L432 345.4l36.7-36.7c6.2-6.2 16.4-6.2 22.6 0s6.2 16.4 0 22.6z"/></svg>'
    else:
        return '<svg class="iconGreen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M544 0c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V32c0-17.7 14.3-32 32-32zM416 96c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V128c0-17.7 14.3-32 32-32zM320 224V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V224c0-17.7 14.3-32 32-32s32 14.3 32 32zM160 288c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V320c0-17.7 14.3-32 32-32zM64 416v64c0 17.7-14.3 32-32 32s-32-14.3-32-32V416c0-17.7 14.3-32 32-32s32 14.3 32 32z"/></svg>'