"""
Execute a job frequently at regular intervals to collect the OpenShift Resource metrics
"""
from crontabs import Cron, Tab
from datetime import datetime
from helper import helper
import subprocess

# cron job defination args
def my_job(*args, **kwargs):
    running = helper.generate_file_name('pods_running')  
    failed = helper.generate_file_name('pods_failed') 
    succeeded = helper.generate_file_name('pods_succeeded')
    subprocess.run(['curl','http://localhost:8000/push_to_object_store'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    response = subprocess.run(['python','./interface/interface_push.py',running, failed, succeeded],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)   
    print('args={} kwargs={} running at {}'.format(args, kwargs, datetime.now()))
    print(response)
# will run with a  specified interval synced to the top of the minute
Cron().schedule(
    Tab(name='run_my_job').every(seconds=60).run(my_job, 'my_arg', my_kwarg='hello')
).go()
