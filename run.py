import akamai
import dcip

"""This will grab the latest DCIP list and upload it to the "TAG DCIP List" in Akamai"""

#TAG section
key = dcip.create_session()
print(f"Session key: {key}")

object_id = dcip.get_object_id(key)
print(f"Object ID: {object_id}")

doc_id = dcip.get_doc_id(object_id, key)
print(f"Document ID: {doc_id}")

dcip.download_list(doc_id, key)

#AKAMAI section
#Get sync point and unique ID of the target network list
search_term = "TAG DCIP"
sync_point, unique_id = akamai.get_list_info(search_term)
print(sync_point)
print(unique_id)

#Get the latest DCIP list using dcip.py
dcip_list = akamai.list_cleanup()
akamai.update_list(dcip_list, sync_point, unique_id)

#Activate the list in production
akamai.activate_list(unique_id)
