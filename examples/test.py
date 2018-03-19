#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import time, sys
reload(sys)
sys.setdefaultencoding('utf8')
import yaml
from InstagramAPI import InstagramAPI
import proxy

username="Isaaclmediauser1774"
pwd="11111password"

configFile= '/root/python/Instagram-API-python/examples/ins.yaml'
stream = file(configFile, 'r')
data = yaml.load(stream)

for user in data["users"]:
    proxyIp = proxy.get_proxy()
    api = InstagramAPI(user["username"], user["password"])
    api.setProxy(proxy = proxyIp)
    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        print(api.LastJson)  # print last response JSON
        print("Login succes! info=" + str(user))
    else:
        print(str(api.LastJson) + ", info=" + str(user))
        print("Can't login!")
    time.sleep(15)
