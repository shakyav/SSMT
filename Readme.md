# SSMT 

OpenShift on OpenStack Metering 

SSMT is python flask web application to get all the OpenShift resource metrics, push it onto the OpenStack Object Store. 


## Requirements

Should have python virtual environment [setup](https://www.tutorialspoint.com/python-virtual-environment)

##### Local Environment 

Should have Minishift cluster up and running


Should be able to access OpenShift cluster using openshift-client 
```
example: oc get pods
```


##### OpenShift Cluster

Should have OpenShift Account

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install python dependencies.

```bash
pip3 install flask 
pip3 install kubernetes
pip3 install openshift
pip3 install crontabs
```

## 
## Environment Variables

```
# To configure object store
export access_key = <access_key>
export secret_key = <secret_key>
export end_point = <authentication endpoint> 
# To configure flask web application 
export host = <hostname> # if not provided, sets the default value
export port = <desired port to run the application> # if not provided, sets the default value
```

## 
## Usage

```python
python3 app.py # will start the flask web application 
python3 crontab.py # will query for the data at periodic intervals
```
Flask Web Application Overview

Try to access the web application URL using the following commands

Local Development

```bash
http://0.0.0.0:9000/push_to_object_store/
# Purpose : Retrieve OpenShift Cluster resource metics and push it to OpenStack Object Store 
# Returns : A list of CSV files pushed to the OpenStack Object Store


http://0.0.0.0:8000/get_cumulative_information/
# Purpose: Retrieve Cumulative infomation like OpenShift Nodes, Pods, PVC's, Projects etc.
# Returns: JSON Response with names of all Nodes, Pods, PVC's, PV's, Projects in an OpenShift cluster

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)