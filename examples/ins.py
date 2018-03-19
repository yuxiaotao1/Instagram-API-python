#ins robots, main script
#coding='utf-8'
#__author__=='0han'
#__email__=='0han@protonmail.com'
#__data__=='2017.8'
import requests,re,json,time,os,os.path,sys
from random import *
from bs4 import BeautifulSoup
import proxy
import dic
import get_pic
from requests_toolbelt import MultipartEncoder
import time, sys
reload(sys)
sys.setdefaultencoding('utf8')
from InstagramAPI import InstagramAPI


class register():
		_session=None
		
		def __init__(self, proxyIp):
			self.proxyIp = proxyIp;
			self.use_proxy = {"http": proxyIp};
			print("==Instagram-robots-account-generate==\n[*] start")
			
		def first_get(self):
			global _session
			_session=requests.session()
			main_url='https://www.instagram.com'
                        print(self.use_proxy)
			_session.get(main_url,proxies=self.use_proxy,verify=True)
			self.save_cookies()
			if os.path.exists('cookiefile'):#print('have cookies')
				self.csrf=self.read_cookies()
				self.data=self.create_ajax()
				print(self.data)
				self.ins()
				time.sleep(5)#wait for 5 seconds
				self.my_selfie=get_pic.get_pic()#
				self.my_selfie.get_selfie()#download random selfie picture to local folder
				self.upload()#upload the selfie
			else:
				pass
		def get_emailaddress(self):#
			email_url="https://10minutemail.net"
			r=requests.get(email_url,verify=False)
			r.encoding='utf-8'
			soup = BeautifulSoup(r.text, 'html.parser')
			return soup.input["value"]
		def generate_FullName(self):
			nameList=dic.data['name']#
			name=nameList[randint(1,12)]
			return name
		def create_username(self):
			username_url="http://namegenerators.org/username-generator/"
			data={'keyword':self.f_name,"numlines":"70","formsubmit":"Generate Username"}
			r=requests.post(username_url,data=data,verify=False)
			r.encoding='utf-8'
			soup=BeautifulSoup(r.text,'html.parser')
			result=soup.select(".section > div:nth-of-type("+str(randint(1,69))+")")[0].string
			result=str(result)+"user"+str(randint(1,2000))
			return result
		
		def create_ajax(self):
			self.email=self.get_emailaddress()
			self.f_name=self.generate_FullName()
			self.passwd=self.f_name+'password'
			self.u_name=self.create_username()
			r_data={
				'email': self.email, #
				'password': self.passwd,#
				'username':self.u_name,#
				'first_name': self.f_name#
				}
			return r_data
		def save_cookies(self):
			global _session,path_for
			with open('./'+"cookiefile",'w')as f:
				json.dump(_session.cookies.get_dict(),f)#_session.cookies.save()
		def read_cookies(self):
			global _session,path_for
			#_session.cookies.load()
			#_session.headers.update(header_data)
			with open('./'+'cookiefile')as f:
				cookie=json.load(f)
				_session.cookies.update(cookie)
				return cookie["csrftoken"]
		def save_account_info(self,username,password):
			with open("account_info.py", "a+") as a:
			    a.write("\n['"+username+"','"+password+"'],")
			print("[*] Successful save the account info")
		def upload(self):
			api = InstagramAPI(self.u_name, self.passwd);
			api.setProxy(proxy = self.proxyIp)
			api.uploadProfilePic("./selfie/1.jpg")
			#global _session
			#file={"file":open("/Users/yxt/code/work/python/ins-account/selfie/1.jpg","rb")}
            #            file={'profile_pic':('profilepic.jpg', open('./selfie/1.jpg','rb'), 'image/jpeg')}
            #            m = MultipartEncoder(file, boundary="----WebKitFormBoundaryElZwUj6xt3tDzqBy")
			#post_selfie_url="https://www.instagram.com/accounts/web_change_profile_picture/"
			#header={
			#	"Accept":"*/*",
			#	"accept-encoding":"gzip, deflate, br",
			#	"Content-Type": m.content_type,
			#	"accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
			#	"origin":"https://www.instagram.com",
			#	"referer":"https://www.instagram.com/",
			#	"user-Agent":dic.data["user_agent"],
			#	"X-csrftoken":self.csrf,
			#	"X-Instagram-AJAX":"1",
			#	"X-Requested-With":"XMLHttpRequest",
			#	}
            #            print(header)
			#r=_session.post(post_selfie_url,headers=header,proxies=self.use_proxy,data=m.to_string(),verify=False)
			#print(r)

		def ins(self):
			global _session
			posturl='https://www.instagram.com/accounts/web_create_ajax/'
			header={
				"Accept":"*/*",
				"accept-encoding":"gzip, deflate, br",
				"Content-Type":"application/x-www-form-urlencoded",
				"accept-language":"zh-CN,zh;q=0.8,en;q=0.6",
				"origin":"https://www.instagram.com",
				"referer":"https://www.instagram.com/",
				"user-Agent":dic.data["user_agent"],
				"X-csrftoken":self.csrf,
				"X-Instagram-AJAX":"1",
				"X-Requested-With":"XMLHttpRequest",
				}		
			r = _session.post(posturl,data=self.data,headers=header,proxies=self.use_proxy,verify=False)#proxies=self.use_proxy
			if r.ok==True:
				print("[*] Sucessful create an account")
				self.save_account_info(self.u_name,self.passwd)
			else:
				print("[x] Unknown Error Occurs!")


proxyIp = proxy.get_proxy()
userReg = register(proxyIp)

for i in range(5):
    # user register
    print("process " + str(i))
    userReg.first_get()
    time.sleep(5)

    # user varify
    print("begin to login : u=" + userReg.u_name + ", p=" + userReg.passwd)
    api = InstagramAPI(userReg.u_name, userReg.passwd);
    api.setProxy(proxyIp)
    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        print(api.LastJson)  # print last response JSON
        print("Login succes! info=" + str(userReg.data))
    else:
        print(str(api.LastJson) + ", info=" + str(userReg.data))
        print("Can't login!")

    time.sleep(25)
