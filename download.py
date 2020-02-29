
import requests
from bs4 import BeautifulSoup
import json,sys
usrag = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
from pymongo import MongoClient
import webbrowser
from getFileSize import getFileSize


client = MongoClient("localhost")["flickr"]


def getHDLink(url,name):
    pg=requests.get(url,headers={"User-Agent":usrag})
    html = BeautifulSoup(pg.text,"html.parser")

    print(pg.status_code)

    sbody=html.find("script",{"class":"modelExport"}).text.split("modelExport: ")[1].split("auth: auth,")[0][:-1].strip()[:-1]

    data= json.loads(sbody)

    imgs=data["main"]["photo-models"][0]["sizes"]
    title= data["main"]["photo-head-meta-models"][0]["title"]
    desc= data["main"]["photo-head-meta-models"][0]["og:description"]
    dttime = data["main"]["photo-models"][0]["owner"]["dateCreated"]
    isHD=data["main"]["photo-models"][0]["isHD"]

    viewCount = data["main"]["photo-models"][0]["engagement"]["viewCount"]

    imgs=sorted(imgs.items(),key=lambda x: x[1]["width"]+x[1]["height"],reverse=True)

    img = "https:"+imgs[0][1]["displayUrl"]
    width = imgs[0][1]["width"]
    height = imgs[0][1]["height"]

    try:
        fsz = getFileSize(img)
    except Exception as e:
        fsz=-1

    client[name].insert_one({"_id":url,"img":img,"collection":name,"width":width,"height":height,"totalsize":width+height,"viewed":False,"title":title.lower(),"desc":desc.lower(),"time":int(dttime),"isHD":isHD,"views":viewCount,"fsz":fsz})
    print(name,img)



def fromScript(url,name):
    try:
        url2=list(client[name].find({"_id":url}))[0]["img"]
        print(url2)

        print("already downloaded")

        # webbrowser.open(url2)
    except Exception as e:
        getHDLink(url,name)


if __name__ == "__main__":
    url,name = input("Enter single url,name:").split(",")

    try:
        url2=list(client[name].find({"_id":url}))[0]["img"]
        print(url2)

        print("already downloaded")

        # webbrowser.open(url2)
    except Exception as e:
        getHDLink(url,name)