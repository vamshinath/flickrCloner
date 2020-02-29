import requests
from bs4 import BeautifulSoup
import json,sys
from pymongo import MongoClient
from selenium import webdriver
import os
from download import fromScript
import time
usrag = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

client = MongoClient("localhost")["flickr"]["links"]

chrome = webdriver.Chrome("/home/kdemac/chromedriver")

def scrollEnd():
    current = chrome.execute_script("return document.body.scrollHeight")
    chrome.execute_script("window.scrollTo(0, {})".format(current))
    time.sleep(2.74)
    new = chrome.execute_script("return document.body.scrollHeight")
    if current == new:
        print("reached end")
    else:
        scrollEnd()


def fetchLinks(url,name,raw):
    # pg=requests.get(url,headers={"User-Agent":usrag})
    # html = BeautifulSoup(pg.text,"html.parser")

    chrome.get(url)

    urlpart = raw.split("flickr.com")[1]
    print(urlpart)
    #aas=html.findAll("a",{"aria-level":"3"})

    scrollEnd()

    aas=chrome.find_elements_by_tag_name("a")

    paas = list(filter(lambda x: urlpart in x.get_attribute("href") and not "page" in x.get_attribute("href") and not "comments" in x.get_attribute("href"),aas))
    
    print(paas)

    for a in paas:
        try:
            urlr = a.get_attribute("href")
            print(urlr)
            fromScript(urlr,name)
        except Exception as e:
            print(e)

    

url,name,last=input().split(",")
try:
    url2=list(client.find({"_id":url}))[0]["links"]
    print(url2)
    print("already downloaded")
except Exception as e:
    for i in range(1,int(last)+1):
        purl = url+"page"+str(i)
        fetchLinks(purl,name,url)
    chrome.close()
    client.insert_one({"_id":url,"links":"done"})
