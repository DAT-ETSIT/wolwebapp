from flask import Flask, render_template
from subprocess import call
from markupsafe import escape
import json

app = Flask(__name__)

machines = []

@app.route('/')
def machineRoute():
    with open('./machines.json', 'r') as file:
        machines = json.load(file)
    
    return render_template('machines.html', machines=machines)

@app.route('/wol/<int:machineId>')
def wolMachine(machineId):
    call(['wakeonlan', '-p', machines[machineId]["port"], machines[machineId]["mac"]])
    return machineRoute()

if __name__ == "__main__":
    app.run(host="192.168.1.21", port=3000, debug=True)