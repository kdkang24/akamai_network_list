from config import BaseConfig as config
from edgegrid import EdgeGridAuth
import json
import requests
import pprint
import datetime


baseurl = '<YOUR_AKAMAI_API_HOST>'
s = requests.Session()
s.auth = EdgeGridAuth(
    client_token='<YOUR_AKAMAI_CLIENT_TOKEN>',
    client_secret='<YOUR_AKAMAI_CLIENT_SECRET>',
    access_token='<YOUR_AKAMAI_ACCESS_TOKEN>'
)
date = datetime.datetime.now()
month = date.strftime("%B")
year = date.strftime("%Y")
notification_email = '<YOUR_EMAIL_ADDRESS_HERE>'

def get_list_info(search_term):
    #In order to update a list, you first need to get its unique ID and sync point
    #you can use the API to search for the names of lists to get more detailed info
    # search_term = "TAG DCIP"
    endpoint = f"{baseurl}/network-list/v2/network-lists"
    payload = {"listType": "IP", "search": search_term}
    result = s.get(endpoint, params=payload)
    print("Get list info status code:", result.status_code)
    data = result.json()
    sync_point = data['networkLists'][0]['syncPoint']
    unique_id = data['networkLists'][0]['uniqueId']
    #Use line below when testing for a different list
    pprint.pprint(result.json())
    return sync_point, unique_id


def update_list(new_dcip_list, sync_point, unique_id):
    #Update the list with the desired info
    #Requires the following parameters: name, type, description, syncPoint, and list
    endpoint = f"{baseurl}/network-list/v2/network-lists/{unique_id}"
    headers = {"Content-Type": "application/json"}
    params = {"extended": "false", "includeElements": "true"}
    data = {
    "name": "TAG DCIP List",
    "type": "IP",
    "description": f"Updated DCIP list for {month} {year}",
    "syncPoint": sync_point,
    "list": new_dcip_list
    }
    result = s.put(endpoint, headers=headers, json=data)
    print("Update list status code:", result.status_code)
    return result.json()

def activate_list(unique_id):
    """Activate the list in the production environment"""
    endpoint = f"{baseurl}/network-list/v2/network-lists/{unique_id}/environments/PRODUCTION/activate"
    headers = {"Content-Type": "application/json"}
    data = {
    "comments": f"New DCIP list for {month} {year}",
    "notificationRecipients": [notification_email]
    }
    result = s.post(endpoint, headers=headers, json=data)
    print("Activate list status code:", result.status_code)
    #Use line below when testing
    #print(result.json())

def list_cleanup():
    """Takes the dcip_list.csv and removes newlines"""
    with open("dcip_list.csv", "r") as file_handle:
        ip_list = file_handle.readlines()
        #Remove the trailing newline after all IPs in list
        #Also remove any blank lines
        clean_list = [ x.rstrip() for x in ip_list if x != "\n"]
    return clean_list


#This function will return a network list object, but it is not needed for this task
"""
def get_network_list():
    endpoint = f"{baseurl}/network-list/v2/network-lists/{unique_id}"
    headers = {"Content-Type": "application/json"}
    params = {"includeElements": "true", "extended": "false"}
    result = s.get(endpoint, headers=headers, params=params)
    print("Get network list status code:", result.status_code)
    return result.json()
"""





