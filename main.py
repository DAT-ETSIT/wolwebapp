from flask import Flask, render_template, request, redirect, url_for
from subprocess import call
from markupsafe import escape
import json

app = Flask(__name__)

with open('./machines.json', 'r') as file:
    machines = json.load(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with open('./machines.json', 'r') as file:
            machines = json.load(file)
        return render_template('machines.html', machines=machines)
    
    elif request.method == 'POST':
        new_machines = []
        for i in range(0,int((len(request.form)-1)/3)):
            new_machines.append({"name": request.form[f"machine[{i}][name]"], "mac": request.form[f"machine[{i}][mac]"], "ip": request.form[f"machine[{i}][ip]"], "port": "7"})
        with open('./machines.json', 'w') as file:
            file.write(json.dumps(new_machines, ensure_ascii=False))
            
        return redirect(url_for('index'))

@app.route('/edit')
def machineEdit():
    with open('./machines.json', 'r') as file:
        machines = json.load(file)
    
    return render_template('editMachines.html', machines=machines)

@app.route('/wol/<int:machineId>')
def wolMachine(machineId):
    call(['wakeonlan', '-p', machines[machineId]["port"], machines[machineId]["mac"]])
    return redirect(url_for('index'))