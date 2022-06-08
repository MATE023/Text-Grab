import os
import uuid
import sys
from azure.storage.blob import BlockBlobService, PublicAccess

ACCOUNT_NAME = "*****************"
ACCOUNT_KEY = "************************"

block_blob_service = BlockBlobService(
    account_name=ACCOUNT_NAME, account_key=ACCOUNT_KEY)

container_name = "words"

block_blob_service.set_container_acl(
    container_name, public_access=PublicAccess.Container)

def upload_file(filename):
    try:
        #local_path = os.path.expanduser("~\Image")
        local_path = os.getcwd()
        #print(local_path)
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("~\Image"))
        full_path = os.path.join(local_path, filename)
    
        block_blob_service.create_blob_from_path(
            container_name, filename, full_path)
        
    except Exception as e:
        print(e)
    
