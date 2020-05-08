import os
from kubernetes import client, config
from openshift.dynamic import DynamicClient
from helper import helper


class ServiceClass(object):
    def __init__(self):
    # to run inside the openshift cluster
        if "OPENSHIFT_BUILD_NAME" in os.environ:
            service_account_path = '/var/run/secrets/kubernetes.io/serviceaccount'

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
        projects_api = self.oapi_client.resources.get(kind='Project', api_version='v1')
        project_list = projects_api.get()
        return [project.metadata.name for project in project_list.items]
    
    def get_running_pods(self):
        pods_api = self.oapi_client.resources.get(kind='Pod', api_version='v1')
        pod_list = pods_api.get()
        return [pod.metadata.name for pod in pod_list.items]

    def get_nodes(self):
        node_api = self.oapi_client.resources.get(kind='Node', api_version='v1')
        node_list = node_api.get()
        return [node.metadata.name for node in node_list.items]
    
    def get_pv(self):
        pvc_api = self.oapi_client.resources.get(kind='PersistentVolume', api_version='v1')
        pvc_list = pvc_api.get()
        return [pv.metadata.name for pv in pvc_list.items]

    def get_pvcs(self):
        pvc_api = self.oapi_client.resources.get(kind='PersistentVolumeClaim', api_version='v1')
        pvc_list = pvc_api.get()
        return [pvc.metadata.name for pvc in pvc_list.items]

    def get_self(self):
        return os.environ.get("HOSTNAME")

    def get_routes(self):
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
        pods_running = {}
        pods_succeeded = {}
        pods_failed={}

        for pod in pods.items:
            if(pod.status.phase == 'Running'):
                pod_namespace = pod.metadata.namespace
                pods_running[pod_namespace] =  pods_running.get(pod_namespace, 0) + 1
            elif(pod.status.phase == 'Failed'):
                pod_namespace = pod.metadata.namespace
                pods_failed[pod_namespace] = pods_succeeded.get(pod_namespace, 0) + 1
            elif(pod.status.phase == 'Succeeded'):
                pod_namespace = pod.metadata.namespace
                pods_succeeded[pod_namespace] = pods_failed.get(pod_namespace,0) +1
                
        list_files=[]
        list_files.append(helper.store_file_in_csv('pods_running',pods_running))
        list_files.append(helper.store_file_in_csv('pods_failed',pods_failed))
        list_files.append(helper.store_file_in_csv('pods_succeeded',pods_succeeded))
        return list_files


        