#Get_Proxy_list by 0han
#date="2017.4.29"
#coding:utf-8 python 3.5
import requests
import time, json

# get proxy
def get_proxy():
        count = 5
        lastRes = ""
        while(count > 0):
            try:
                s=requests.session()
                print("[*] Get Annoymous IP Proxy")
                mainurl="https://gimmeproxy.com/api/getProxy"
                r=s.get(mainurl,verify=True)
                lastRes = r.text
                dic=json.loads(r.text)
                proxyServer = dic["curl"]
                dic_main={"https": proxyServer, "http": proxyServer}
                print("result:" + proxyServer)
                url='https://api.ipify.org?format=json'
                res=s.get(url,proxies=dic_main,verify=True)
                dic=json.loads(res.text)
                print(dic["ip"])
                return proxyServer
            except Exception as e:
                print("proxy exception:" + str(e) + ":" + lastRes)
                time.sleep(5)
