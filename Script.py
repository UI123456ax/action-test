import requests
import re, json
from lxml import etree
import os
# from Tools.Spider_tools import Unicode

FLARESOLVERR_URL = "http://localhost:8191/v1"
FLARESOLVERR_HEADERS = {"Content-Type": "application/json"}

DEBUG = True 

def Unicode(escaped_string):
    '''Unicode文本解码'''
    import re
    def unescape_unicode(match):  
        return chr(int(match.group(1), 16))  
    unescaped_string = re.sub(r'\\u([0-9a-fA-F]{4})', unescape_unicode, escaped_string)  
    return unescaped_string

class Jmcomic():
    def __init__(self, username='', password='', cookies=None, session=None):
        self.__username = username
        self.__password = password
        self.session = session or self._create_flaresolverr_session()
        print(f'初始化请求头:{self.session.headers}\n初始化Cookies:{self.session.cookies}')
        self.cookies = self.login()

    def _create_flaresolverr_session(self):
        """创建通过FlareSolverr的session"""
        data = {
            "cmd": "request.get",
            "url": "https://18comic.vip/",
            "maxTimeout": 160000
        }
        response = requests.post(FLARESOLVERR_URL, 
                               headers=FLARESOLVERR_HEADERS, 
                               json=data)
        
        if response.status_code != 200:
            raise Exception(f"FlareSolverr请求失败: {response.text}")
            
        solution = response.json()['solution']
        session = requests.Session()
        session.headers.update({"User-Agent": solution['userAgent']})
        
        # 设置cookies
        cookies = {c['name']: c['value'] for c in solution['cookies']}
        session.cookies.update(cookies)
        
        if DEBUG: 
            print('初始响应(前100字符):', solution['response'][:100])
        return session

    # 选择分流
    def shunt(self):
        return ['https://18comic.vip']

    # 登录
    def login(self):
        get_shunt = self.shunt()
        self.shunt_url = get_shunt[0]
        print('当前请求分流 --> ' + self.shunt_url)
        
        # 通过FlareSolverr发送登录请求
        data = {
            "cmd": "request.post",
            "url": self.shunt_url + "/login",
            "postData": f"username={self.__username}&password={self.__password}&submit_login=1",
            "headers": {
                "origin": self.shunt_url,
                "referer": self.shunt_url,
                "Connection": "close"
            },
            "maxTimeout": 160000
        }
        
        response = requests.post(FLARESOLVERR_URL, 
                              headers=FLARESOLVERR_HEADERS, 
                              json=data)
        
        if response.status_code != 200:
            raise Exception(f"登录请求失败: {response.text}")
            
        solution = response.json()['solution']
        if DEBUG: 
            print('登录响应(前100字符):', solution['response'][:100])
            print('Cookies:\n', solution['cookies'])
        
        # 更新session的cookies
        cookies = {c['name']: c['value'] for c in solution['cookies']}
        self.session.cookies.update(cookies)
        return cookies

    # 签到 + 10Exp + 5Gold
    def check_in(self):
        data = {
            "cmd": "request.post",
            "url": self.shunt_url + "/ajax/user_daily_sign",
            "postData": f"daily_id=47&oldStep=1",
            "maxTimeout": 160000
        }
        response = requests.post(FLARESOLVERR_URL,
                              headers=FLARESOLVERR_HEADERS,
                              json=data)
        if response.status_code != 200:
            raise Exception(f"签到请求失败: {response.text}")
        print(response.json()['solution']['response'])

    # 广告 + 5Exp(2) + 5Gold(5)
    def ad_check(self):  
        g = 0
        e = 0
        while True:
            data = {
                "cmd": "request.get",
                "url": self.shunt_url + "/ajax/ad_check",
                "maxTimeout": 160000
            }
            response = requests.post(FLARESOLVERR_URL,
                                  headers=FLARESOLVERR_HEADERS,
                                  json=data)
            if response.status_code != 200:
                raise Exception(f"广告请求失败: {response.text}")
                
            msg = response.json()['solution']['response']
            if DEBUG:
                print(Unicode(msg))
            # gold
            if '\u91d1\u5e63' in msg:
                g += 5
            # exp
            if '\u7d93\u9a57\u503c' in msg:
                e += 5
            # End
            if msg in '':
                break
        print(f'已完成每日廣告點擊: 獲得「{g}」金幣、「{e}」經驗值')

    # 喜欢作品 + 5Exp 存在漏洞(取消album_id、referer，再次正常请求)
    def like_check(self):
        for i in range(4):
            data = {
                "cmd": "request.post",
                "url": self.shunt_url + "/ajax/vote_album",
                "postData": f"album_id={313827+i}&vote=likes",
                "maxTimeout": 160000
            }
            response = requests.post(FLARESOLVERR_URL,
                                   headers=FLARESOLVERR_HEADERS,
                                   json=data)
            if response.status_code != 200:
                raise Exception(f"点赞请求失败: {response.text}")
            if DEBUG: print(response.json()['solution']['response'])
            print(f'ID {313827+i}: {response.json()["solution"]["response"]}')

    # 获取漫画
    def get_comic(self):
        pass

    # Action
    def action(self):
        self.check_in()
        self.ad_check()
        self.like_check()    


def Information():
    web = 'https://jmcomicgo.xyz/'
    environ = 'JMCOMIC'
    return [web,environ]

def Main(username,password,cookies=None):
    global DEBUG; DEBUG = True
    Jmcomic(username,password,cookies).action()


if __name__ == '__main__':
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    cookies = None
    Jmcomic(username,password,cookies).action()
