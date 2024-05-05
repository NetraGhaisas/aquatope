import requests
import json

def handle(req):
    # Define the URLs of the OpenFaaS functions
    function1_url = "http://gateway.openfaas:8080/function/social-network-compose-post"
    function2_url = "http://gateway.openfaas:8080/function/social-network-store-post"
    function3_url = "http://gateway.openfaas:8080/function/social-network-read-social-graph"
    function4_url = "http://gateway.openfaas:8080/function/social-network-write-home-timeline"

    try:
        # Make HTTP request to function 1
        response1 = requests.post(function1_url, data=req)
        response1.raise_for_status()
        result1 = response1.json()

        # Make HTTP request to function 2 with the result from function 1
        response2 = requests.post(function2_url, data=json.dumps(result1))
        response2.raise_for_status()
        result2 = response2.json()

        # Make HTTP request to function 2 with the result from function 1
        response3 = requests.post(function3_url, data=json.dumps(result1))
        response3.raise_for_status()
        result3 = response3.json()

        # Make HTTP request to function 2 with the result from function 1
        response4 = requests.post(function4_url, data=json.dumps(result3))
        response4.raise_for_status()
        result4 = response4.json()

        return result4

    except Exception as e:
        return str(e)
