"""
app.py is the flask application and provides a rest end point to frontend applicaiton
"""
from flask import Flask
from flask import request
from api import openshift_info
from flask.json import jsonify
import signal
import os
import sys

app = Flask(__name__)

openshift_object = openshift_info.ServiceClass()

@app.route('/push_to_object_store')
def push_to_object_store():
    """
    flask application code to retreive, store the data in csv
    """
    list_my = openshift_object.get_all()
    return jsonify(list_my)

@app.route('/get_cumulative_information')
def main():
    """
    flask application code to retreive, pods, nodes, services, pvc
    """
    pods = openshift_object.get_running_pods()
    me = openshift_object.get_self()
    routes = openshift_object.get_routes()
    nodes = openshift_object.get_nodes()
    pvc = openshift_object.get_pvcs()
    pv = openshift_object.get_pv()
    project = openshift_object.get_projects()
    return jsonify({
            "pods": pods,
            "me": me,
            "routes": routes, 
            "nodes":nodes,
            "pvcs":pvc,
            "pv":pv,
            "projects":project})

def signal_term_handler(signal, frame):
    app.logger.warn('got SIGTERM')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    
    app.run(host=str(os.environ.get("HOST","localhost")), port=int(os.environ.get("PORT", 8000)))
