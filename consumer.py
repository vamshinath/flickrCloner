from pymongo import MongoClient
import webbrowser
import humanize
visited=[]

from selenium import webdriver

chrome = webdriver.Chrome("/home/kdemac/chromedriver")

client = MongoClient("localhost")["flickr"]

print(client.list_collection_names())

ct = input("Enter Collection Name:")

searchKeys={"1":"title","2":"desc"}
print(searchKeys)
searchKey = input("Enter SearchKey:")
sterm = input("Enter searchTerm:")

dontterm = input("Enter dont term:")

skeys = {"1":"fsz","2":"width","3":"height","4":"time","5":"totalsize","6":"total/fsz","7":"views"}

print(skeys)

skey = input("Enter sort key:")

skey = "1" if skey == "" else skey

reverser = input("Enter y for asc:") == "y"



def printe(im):
    print(im["_id"])
    print(im["views"])
    print(im["title"])
    print(im["desc"])
    print(im["width"],im["height"])
    print(humanize.naturalsize(im["fsz"]))
    print()
    print(len(imgs))


if ct != "":
    if searchKey == "":
        imgs=list(client[ct].find({"viewed":False}))
    else:
        imgs=list(client[ct].find({"viewed":False,searchKeys[searchKey]:{"$regex":sterm}}))


else:
    cts = client.list_collection_names()
    cts.remove("links")
    imgs=[]
    for ct in cts:
        if searchKey == "":
            imgs+=list(client[ct].find({"viewed":False}))
        else:
            imgs+=list(client[ct].find({"viewed":False,searchKeys[searchKey]:{"$regex":sterm}}))

if skey != "6":
    imgs=sorted(imgs,key=lambda x:x[skeys[skey]],reverse=True)
else:
    imgs=sorted(imgs,key=lambda x:x["fsz"]/x["totalsize"],reverse=True)


while len(imgs):
    im = imgs.pop(0)
    if dontterm in im["title"]:
        continue
    url = im["img"]
    if url in visited:
        continue
    chrome.get(url)
    printe(im)
    input()
    client[im["collection"]].update_one({"_id":im["_id"]},{"$set":{"viewed":True}})
    visited.append(url)

chrome.close()