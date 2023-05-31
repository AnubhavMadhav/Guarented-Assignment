# pip3 install b2sdk
# pip3 install mongoengine

import os
from b2sdk.v2 import B2Api
from mongoengine import *

# Input of item_id
item_id = "item7"
folder_path = "/Users/testbook/Desktop/Guarented-Assignment/dirs"

# Configure Backblaze B2
application_key_id = "005b70cb5a4f9780000000001"
# application keyName = "AnubhavBackblaze"
application_key = "K005ZMH4Q+KcxmDdD9ttu2KdIuzofvY"
bucket_name = "BucketAnubhav"
# bucket_id = "db67407c8b656ae48f890718"

# Authenticate with Backblaze B2
b2_api = B2Api()
b2_api.authorize_account("production", application_key_id, application_key)

# Connect to the MongoDB - mongoengine
con = connect(db="Items", username='anubhavmadhav', password='pKR4S51CO3O2CoTy', host='mongodb+srv://anubhavmadhav:pKR4S51CO3O2CoTy@anubhavcluster.2lskq03.mongodb.net/Items', port=27017)
# print("con : ", con)

# get DataBase
# db = get_db()
# print("database name : ", db.name)

# get collections
# collections = con.list_collection_names()
# for collection in collections:
#    print(collection)

# Define the MongoDB model using mongoengine
class Item(Document):
    item_id = StringField(unique=True)
    images = ListField(StringField())

    def _init_(self, id, urls):
      self.item_id = id,
      self.images=urls

# get objects present in the DB
for item in Item.objects:
    print("itemId : ", item.item_id, " images : ", item.images)


# Function to upload a file to Backblaze B2 and return the public URL
def upload_file(file_path, bucket, item_id):
    file_name = os.path.basename(file_path)
    file_data = open(file_path, "rb")

    response = bucket.upload_bytes(file_data.read(), item_id + "/" + file_name)
    file_data.close()
    print("response : ", response)

    # Construct the public URL
    public_url = f"https://f005.backblazeb2.com/file/{bucket_name}/{file_name}"

    return public_url


# Upload files to Backblaze B2
def upload_files_to_b2(item_id, folder_path):
    bucket = b2_api.get_bucket_by_name(bucket_name)
    folder_path = folder_path + "/" + item_id

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        public_url = upload_file(file_path, bucket, item_id)

        # Store the public URL in the MongoDB database
        item = Item.objects(item_id=item_id).first()
        if item is None:
            item = Item(item_id=item_id)
        item.images.append(public_url)
        item.save()

upload_files_to_b2(item_id, folder_path)
