#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:24:20 2019

@author: moi
"""

import requests, pprint, os

from pymongo import MongoClient # librairie qui va bien
import configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))

CNF = "mongo"
BDD = "Datalab"

# Ouverture connection -> mongo sur serveur
client = MongoClient('mongodb://%s:%s@%s/?authSource=%s' % (config[CNF]['user'], config[CNF]['password'], config[CNF]['host'], BDD))
print(client)

bdd = client['Datalab'] # BDD "Datalab" de mongoDB sur serveur
bdd
print("'MOOC_GRP_MAN' Collections:")
for cn in bdd.list_collection_names():
    print("-"+cn)
collec = client['MOOC_GRP_MAN']['fringilla_vigo']

#~ exit()

response = requests.get(
    "https://www.fun-mooc.fr/courses/course-v1:UCA+107001+session02/discussion/forum/i4x-UCA-course-107001-session02/threads/5b8fecac1c89dc02ae0030e7?ajax=1&resp_skip=0&resp_limit=999",
    #params={'q': 'requests+language:python'},
    #headers={'Accept': 'application/vnd.github.v3.text-match+json'},
    headers={
        #"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language": "en-US,en;q=0.5",
        "X-CSRFToken": "M4pngh0I3u81T4McYr38hLzJjwpBAiVv", #Change à chaque fois!!!!
        "X-Requested-With": "XMLHttpRequest",
        #'Referer': 'https://www.fun-mooc.fr/courses/course-v1:MinesTelecom+04026+session05/discussion/forum/204c764cf87424d86a6259562d1d200afe30ab9a/threads/5d9481db1c89dcf269015b6f' ,
        'Cookie': 'Cookie: defaultRes=900%2C0; csrftoken=M4pngh0I3u81T4McYr38hLzJjwpBAiVv; atuserid=%7B%22name%22%3A%22atuserid%22%2C%22val%22%3A%222bcd8684-307f-4536-8925-aef21cd909ff%22%2C%22options%22%3A%7B%22end%22%3A%222020-11-02T08%3A43%3A21.983Z%22%2C%22path%22%3A%22%2F%22%7D%7D; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-602676-%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; sessionid=xh3lf4oa1xsdnjukvsf25zvx1scyib69; edxloggedin=true; edx-user-info="{\"username\": \"Gerikk\"\054 \"version\": 1\054 \"email\": \"alexandreblt4@gmail.com\"\054 \"header_urls\": {\"learner_profile\": \"https://www.fun-mooc.fr/u/Gerikk\"\054 \"logout\": \"https://www.fun-mooc.fr/logout\"\054 \"account_settings\": \"https://www.fun-mooc.fr/account/settings\"}}"'
    },
)

print(response.content)
pprint.pprint(response.json())

collec.insert_one(response.json())



for d in response.content:
    test=response.json()


print(response.content)
pprint.pprint(response.json())
Dico=response.json()
