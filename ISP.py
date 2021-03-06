import time
import random
import requests
from bs4 import BeautifulSoup
#from lxml import etree

class ISP():
    def __init__(self):
        self.main_url=""
        self.login_url=""
        self.register_url = ""
        self.function_url=""
        self.headers={"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45"}
        self.login_from_data={
            "login": "login",
            "checkcode": "1",
            "rank": "0",
            "action": "login",
            "m5": "1"
        }
        self.session=requests.session()
    #随机选择服务器
    def server_chose(self):
        server_list=["1-1","1-2","2","2-1","2-2","3","3-1","3-2","4","4-1","4-3"]
        server_name=["民主","文明","和谐","自由","平等","公正","法治","爱国","敬业","诚信","友善"]
        server_index=random.choice(range(11))
        server_chose=server_list[server_index]
        print("选择的服务器为{}".format(server_name[server_index]))
        self.main_url= "https://xsswzx.cdu.edu.cn/ispstu{}/com_user/".format(server_chose)
        self.login_url = self.main_url + "oslogin.asp"
        self.register_url = self.main_url + "project_addx.asp?id={}&id2={}"
        self.function_url = self.main_url + "{}.asp"
    #登录ISP
    def login(self):
        self.server_chose()
        while True:
            self.input_username()
            code_html = self.session.get(self.login_url,headers=self.headers).content
            soup=BeautifulSoup(code_html,"lxml")
            code=soup.select('div .form-bottom div')[2].text[3:7] #解析验证码
            self.login_from_data["code"]=code
            login_data=self.session.post(self.login_url, data=self.login_from_data, headers=self.headers)
            print("学号:{0}\n密码:{1}\n验证码:{2}".format(self.login_from_data["username"], self.login_from_data["userpwd"],self.login_from_data["code"]))
            soup=BeautifulSoup(login_data.content,'lxml')
            if soup.find('title').text=="管理系统":
                page_top=self.session.get(self.function_url.format("top")).content
                user_soup=BeautifulSoup(page_top,"lxml")
                user_name=user_soup.find_all("font")[0].text[5:]
                print(user_name,end=" ")
                print("登录成功！")
                break
            else:
                print("账号或密码错误，请重新输入")
    #提交一键登记
    def register(self):
        left_data = self.session.get(self.function_url.format("left")).content
        soup = BeautifulSoup(left_data, "lxml")
        id = soup.find_all('a')[5]['href'].split('=')[1]
        self.session.get(self.register_url.format(id,time.strftime("%Y年%m月%d日",time.localtime())))  #一键登记链接
    def input_username(self):
        while True:
            username = input("请输入你的学号(输入空值默认上次记录或“user.txt”保存的账号)")
            if username:
                self.login_from_data["username"] = username
                with open("user.txt", "w") as f:
                    f.writelines(username + "\n")
                break
            else:
                try:
                    self.login_from_data["username"] = open("user.txt", "r").readlines()[0][:-1]
                    break
                except:
                    print("请输入账号")
        while True:
            userpwd = input("请输入你的密码(输入控制默认上次记录或“user.txt”保存的账号)")
            if userpwd:
                self.login_from_data["userpwd"] = userpwd
                with open("user.txt", "a") as f:
                    f.writelines(userpwd)
                break
            else:
                try:
                    self.login_from_data["userpwd"] = open("user.txt", "r").readlines()[-1]
                    break
                except:
                    print("请输入密码")
    def start(self):
        self.login()  #登录
        self.register()  #登记
        print("{}登记成功！".format(time.strftime("%Y年%m月%d日")))
#ISP().start()
if __name__ == "__main__":
    print("本程序仅供学习交流，请下载后24h内删除")
    while True:
        ISP().start()
        try:
            flog=eval(input("是否继续，输入1为继续，其余退出程序"))
            if flog==1:
                continue
            else:
                break
        except:
            break
