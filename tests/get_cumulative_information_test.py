import requests

def test_get_cumulative_information_for_openshift_check_status_code():
    response = requests.get("http://localhost:8000/get_cumulative_information")
    response_body = response.json();
    assert response.status_code == 200

def test_get_cumulative_information_for_openshift_check_response_body():
    response = requests.get("http://localhost:8000/get_cumulative_information")
    response_body = response.json();
    assert response.headers['Content-Type'] == "application/json"

def test_get_cumulative_information_for_openshift_check_project():
    response = requests.get("http://localhost:8000/get_cumulative_information")
    response_body = response.json();
    assert response_body["projects"][0] == "default"

def test_push_to_object_store_check_status_code():
    response = requests.get("http://localhost:8000/push_to_object_store")
    response_body = response.json();
    assert response.status_code == 200


