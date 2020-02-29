from getFileSize import getFileSize
from pymongo import MongoClient


client = MongoClient("localhost")["flickr"]

cts = client.list_collection_names()

cts.remove("links")

for ct in cts:
    recs=client[ct].find({"viewed":False})
    print(ct)
    for rec in recs:
        client[ct].update_one({"_id":rec["_id"]},{"$set":{"collection":ct}})
