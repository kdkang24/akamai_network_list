#This script will authenticate and create a session with the TAG API, retrieve the current DCIP list, and download it into a file named dcip_list.csv
import requests
import json
import pprint
import re

#fixed base url
base_url = "https://members.tagtoday.net"
username = '<YOUR_TAG_USERNAME'
password = '<YOUR_TAG_PASSWORD'
app_ID = '<YOUR_TAG_APP_ID>'
app_pass = '<YOUR_TAG_APP_PASSWORD'

def create_session():
    #documentation says /api/api.svc, but it's actually /.api/api.svc
    api_url = f"{base_url}/.api/api.svc/session/create"
    payload = {"appId": app_ID, "AppPass": app_pass, "username": username, "password": password, "community": "members.tagtoday.net", "apiversion": 1}
    r = requests.post(api_url, params=payload)
    session_key = re.findall(r"<sessionKey>(.*?)</sessionKey>", r.text)
    #session keys last for 12 hrs
    print(f"Session key request status: {r.status_code}")
    return session_key[0]

def get_object_id(key):
    """Gets the ID of the folder where the list resides"""
    api_url = f"{base_url}/.api/api.svc/objects/byPath"
    payload = {"domain": "members.tagtoday.net", "path": "/tag_tools/dcip/dcip_files/data_center_ip_monthly_list"}
    headers = {"cookie": f"iglooauth={key}"}
    r = requests.get(api_url, params=payload, headers=headers)
    id = re.findall(r"<id>(.*?)</id><href>/tag_tools/dcip/dcip_files/data_center_ip_monthly_list</href>", r.text)
    print(f"Object ID request status: {r.status_code}")
    return id[0]

def get_doc_id(object_id, key):
    """Gets the ID of the list file"""
    api_url = f"{base_url}/.api/api.svc/folders/{object_id}/children/view"
    payload = {"objectId": f"{object_id}"}
    headers = {"cookie": f"iglooauth={key}"}
    r = requests.get(api_url, params=payload, headers=headers)
    doc = re.findall(r'<object i:type="Document"><id>(.*?)</id><href>/tag_tools/dcip/dcip_files/data_center_ip_monthly_list', r.text)
    print(f"Document ID request status: {r.status_code}")
    return doc[0]

def download_list(doc_id, key):
    """Downloads the file and saves it as dcip_list.csv"""
    api_url = f"{base_url}/.api/api.svc/documents/{doc_id}/view_binary"
    payload = {"documentId": f"{doc_id}"}
    headers = {"cookie": f"iglooauth={key}"}
    r = requests.get(api_url, params=payload, headers=headers)
    print(f"Download list request status: {r.status_code}")
    print(f"Saving list as dcip_list.csv...")
    filehandle = open('dcip_list.csv', 'w')
    filehandle.write(r.text)
    filehandle.close()


#This block has been moved into run.py
"""
key = create_session()
print(f"Session key: {key}")
object_id = get_object_id()
print(f"Object ID: {object_id}")
doc_id = get_doc_id()
print(f"Document ID: {doc_id}")
download_list()
"""



