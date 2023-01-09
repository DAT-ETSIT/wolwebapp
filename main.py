from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_required, login_user, LoginManager

import json
from subprocess import call, run, PIPE
from markupsafe import escape

from database import db, init_db, db_session
from models import User, Machine
from auth import auth
from views import views

login_manager = LoginManager()

app = Flask(__name__)

init_db()

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
        return '<svg class="iconRedX" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M310.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L160 210.7 54.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L114.7 256 9.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 301.3 265.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L205.3 256 310.6 150.6z"/></svg>'
    else:
        return '<svg class="iconGreen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M544 0c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V32c0-17.7 14.3-32 32-32zM416 96c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V128c0-17.7 14.3-32 32-32zM320 224V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V224c0-17.7 14.3-32 32-32s32 14.3 32 32zM160 288c17.7 0 32 14.3 32 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V320c0-17.7 14.3-32 32-32zM64 416v64c0 17.7-14.3 32-32 32s-32-14.3-32-32V416c0-17.7 14.3-32 32-32s32 14.3 32 32z"/></svg>'
