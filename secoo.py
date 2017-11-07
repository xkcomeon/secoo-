#coding=utf-8
import requests
import hashlib
import time
import datetime
import json
from lxml import etree
from rk import *

class Account():
    def __init__(self,username,password,rk_name,rk_pass):
        self.name = username
        self.password = password
        self.rk_name = rk_name
        self.rk_pass = rk_pass
        self.rc = RClient(rk_name, rk_pass)
        self.headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)",
                        'Referer' : 'http://passport.secoo.com/login/',
                        }

    def login(self):
        # 时间戳
        m = hashlib.md5()
        m.update(self.password)
        pwd = m.hexdigest()
        now = datetime.datetime.now()
        print now
        # time_array = time.strptime(now,"%Y-%m-%d %H:%M:%S")
        num_time = time.mktime(now.timetuple())
        num_time = str(int(num_time))
        session = requests.session()
        login_url = 'https://passport.secoo.com/login/Logic_login.jsp'
        captcha_url = 'https://passport.secoo.com/login/graph_captcha.jsp?ume=' + self.name + '&t=' + num_time
        while True:
            response_ca = session.get(captcha_url,headers = self.headers)
            html3 = response_ca.content
            # filename = captcha_url[-10:] + '.jpg'
            # with open(filename,'w') as f:
            #     f.write(html3)
            # captcha = raw_input('请输入识别的验证码：')
            try:
                codex = self.rc.rk_create(html3, 3040)['Result']
            except Exception as err:
                print(err)
                raise Exception("若快验证码识别出错！")
            # print(codex)
            formdata = {
                'userName' : self.name ,
                'passWord' : pwd,
                'capcode' : codex,
                'command' : 'LOGIN',
                'loginType' : '',
            }
            session.get('http://passport.secoo.com/login/',headers=self.headers)
            context = session.post(login_url, data=formdata, headers=self.headers)
            # print context.text
            context = json.loads(context.text)
            if  context['recode'] == 1 or context['recode'] == 0:
                print '登录成功'
                break
            if context['error'] == '用户名或密码不正确':
                print '用户名或密码不正确'
            else:
                print '打码失误，正在重试'
            response = session.get('http://my.secoo.com/order/myorder.jsp', headers=self.headers).text
            response = etree.HTML(response)
            nodes = response.xpath('//head/title/text()')[0]
            # print nodes
            # if u'免费注册' not in nodes:
            #     print 'ok'
            #     break
            # else:
            #     print '打码失误，正在重试'


if __name__ == '__main__':
    a = Account('18613703**','xk****','xkk***','1***')
    a.login()

