"""
openshift_info is a python class where it requests openshift master api to fetch the details.\n
thereafter, it filters the received response and sends to app.py
"""
import os
from kubernetes import client, config
from openshift.dynamic import DynamicClient
from helper import helper


class ServiceClass(object):
    def __init__(self):
        """
        To configure the openshift cluster with the application
        Uses Openshift Client to authenticate with Openshift API 
        """        
        if "OPENSHIFT_BUILD_NAME" in os.environ:
            service_account_path = os.environ.get('service_account_path')

            with open(os.path.join(service_account_path, 'namespace')) as fp:
                self.namespace = fp.read().strip()
            config.load_incluster_config()

            configuration = client.Configuration()
            configuration.verify_ssl = False

            self.oapi_client = DynamicClient(
                client.ApiClient(configuration=configuration)
            )
    # to run in our local environment as well. 
        else:
            config.load_kube_config()
            configuration = client.Configuration()
            configuration.verify_ssl = False
            self.namespace = 'default'
            self.oapi_client = DynamicClient(
                client.ApiClient(configuration=configuration)
            )
    # to get all active, termination projects
    def get_projects(self):
        """
        Purpose: To get all Active, Terminating Projects
        Input: Instance of the class
        Output: Returns a list of all project names in active and terminating state
        """
        projects_api = self.oapi_client.resources.get(kind='Project', api_version='v1')
        project_list = projects_api.get()
        return [project.metadata.name for project in project_list.items]
    
    def get_running_pods(self):
        """
        Purpose: To get all pods in Running, Terminating, Succeeded
        Input: Instance of the class
        Output: Returns a list of all pod names in active and terminating state
        """
        pods_api = self.oapi_client.resources.get(kind='Pod', api_version='v1')
        pod_list = pods_api.get()
        return [pod.metadata.name for pod in pod_list.items]

    def get_nodes(self):
        """
        Purpose: To get all nodes 
        Input: Instance of the class
        Output: Returns a list of names of all OpenShift nodes
        """
        node_api = self.oapi_client.resources.get(kind='Node', api_version='v1')
        node_list = node_api.get()
        return [node.metadata.name for node in node_list.items]
    
    def get_pv(self):
        """
        Purpose: To get all pv
        Input: Instance of the class
        Output: Returns a list of names of all PersistentVolume
        """
        pvc_api = self.oapi_client.resources.get(kind='PersistentVolume', api_version='v1')
        pvc_list = pvc_api.get()
        return [pv.metadata.name for pv in pvc_list.items]

    def get_pvcs(self):
        """
        Purpose: To get all pvc
        Input: Instance of the class
        Output: Returns a list of names of all PersistentVolumeClaim
        """
        pvc_api = self.oapi_client.resources.get(kind='PersistentVolumeClaim', api_version='v1')
        pvc_list = pvc_api.get()
        return [pvc.metadata.name for pvc in pvc_list.items]

    def get_self(self):
        """
        Purpose: To get hostname
        Input: Instance of the class
        Output: Returns Hostname
        """
        return os.environ.get("HOSTNAME")

    def get_routes(self):
        """
        Purpose: To get all routes
        Input: Instance of the class
        Output: Returns a list of all routes (names)
        """
        routes_api = self.oapi_client.resources.get(kind='Route',api_version='route.openshift.io/v1')
        route_list = routes_api.get(namespace=self.namespace)
        return self._get_names(route_list)
    
    def get_all(self):
        pods_api = self.oapi_client.resources.get(kind='Pod', api_version='v1')
        pod_list = pods_api.get()
        return self._get_status_pods(pod_list)

    def _get_names(self, resources):
        return [resource.metadata.name for resource in resources.items]

    def _get_status_pods(self, pods):
        """
        Purpose: Seperate the list of all running, failed and succeeded pods
        Input: Instance of the class and pod item list
        Output: Returns a list of csv filenames where the data is stored
        """
        pods_running = {}
        pods_succeeded = {}
        pods_failed={}
        pods_pending={}
        pods_unknown={}
        for pod in pods.items:
            if(pod.status.phase == 'Running'):
                pod_namespace = pod.metadata.namespace
                pods_running[pod_namespace] =  pods_running.get(pod_namespace, 0) + 1
            elif(pod.status.phase == 'Failed'):
                pod_namespace = pod.metadata.namespace
                pods_failed[pod_namespace] = pods_succeeded.get(pod_namespace, 0) + 1
            elif(pod.status.phase == 'Succeeded'):
                pod_namespace = pod.metadata.namespace
                pods_succeeded[pod_namespace] = pods_failed.get(pod_namespace,0) + 1
            elif(pod.status.phase == 'Pending'):
                pod_namespace = pod.metadata.namespace
                pods_pending[pod_namespace] = pods_pending.get(pod_namespace,0) + 1
            else:
                pod_namespace = pod.metadata.namespace
                pods_unknown[pod_namespace] = pods_unknown.get(pod_namespace,0) + 1               
        list_files=[]
        list_files.append(helper.store_file_in_csv('pods_running',pods_running))
        list_files.append(helper.store_file_in_csv('pods_failed',pods_failed))
        list_files.append(helper.store_file_in_csv('pods_succeeded',pods_succeeded))
        return list_files


        