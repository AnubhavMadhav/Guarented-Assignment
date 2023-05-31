# pip3 install mongoengine

# NOTE: In order to run this file, you are supposed to enter your Credentials for Google Cloud.
# 1. Provide path to your service account key for "GOOGLE_APPLICATION_CREDENTIALS"
# 2. Enter name of the Google Cloud Storage Bucket in "bucket_name"

import os
import asyncio
from google.cloud import storage
from mongoengine import *

# Define the MongoDB model using mongoengine
class Item(Document):
    item_id = StringField(unique=True)
    images = ListField(StringField())

    def _init_(self, id, urls):
      self.item_id = id,
      self.images=urls


# Rough Trial Attempt
# print("dirs : ", os.listdir("/Users/testbook/Desktop/Guarented-Assignment/dirs"))
# item_id = "item1"
# blob_prefix = f"{item_id}/"
# print("blob_prefix : ", blob_prefix)

# Configure Google Cloud Storage Credentials
# Replace this with the path to your service account key json file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/service_account_key.json"
storage_client = storage.Client()


# Asynchronous image upload and database update
async def upload_images(item_id, folder_path, bucket_name):
    bucket = storage_client.bucket(bucket_name)
    blob_prefix = f"{item_id}/"
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        blob_name = blob_prefix + file_name
        blob = bucket.blob(blob_name)
        await blob.upload_from_filename(file_path, timeout=3600)
        
        # Store the public URL in the MongoDB database
        item = await Item.objects.filter(item_id=item_id).first()
        if item is None:
            item = Item(item_id=item_id)
        item.images.append(blob.public_url)
        await item.save()

# Example usage
item_id = "item1"
folder_path = "/Users/testbook/Desktop/Guarented-Assignment/dirs"

# Enter your `bucket_name` here
bucket_name = "<bucket_name>"     

# Create Mongo Connection
con = connect(db="Items", username='anubhavmadhav', password='pKR4S51CO3O2CoTy', host='mongodb+srv://anubhavmadhav:pKR4S51CO3O2CoTy@anubhavcluster.2lskq03.mongodb.net/Items', port=27017)

# Get DB
# db = get_db()
# print("database name : ", db.name)

# Get Collections
# collections = con.list_collection_names()
# for collection in collections:
#    print(collection)


for item in Item.objects:
    print("itemId : ", item.item_id, " images : ", item.images)


# Rough Trial Attempt
# Try inserting in the DB through code
# i1 = Item()
# i1.item_id = 'item6'
# i1.images = ['url7', 'url8', 'url9']
# i1.save()

# Create an event loop
loop = asyncio.get_event_loop()

# Run the upload and database update asynchronously
loop.run_until_complete(upload_images(item_id, folder_path, bucket_name))