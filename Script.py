import requests
import re,json
from lxml import etree
# from Tools.Spider_tools import Unicode

DEBUG = True 

def Unicode(escaped_string):
    '''Unicode文本解码'''
    import re
    def unescape_unicode(match):  
        return chr(int(match.group(1), 16))  
    unescaped_string = re.sub(r'\\u([0-9a-fA-F]{4})', unescape_unicode, escaped_string)  
    return unescaped_string

def check_proxy():
    '''代理检测'''
    import requests
    try:
        response = requests.get('http://httpbin.org/ip', timeout=5)
        if response.status_code == 200:
            address = requests.get(f"https://api.vore.top/api/IPdata?ip={response.json()['origin']}").json()
            print("当前IP地址:", response.json()['origin'])
            if address['code'] != 200: print('地址查询失败')
            else: 
                print(f"{address['ipdata']['info1']}: {address['ipdata']['isp']}")
                print(f"代理模式: {not address['ipinfo']['cnip']}")
                return not address['ipinfo']['cnip']
        else:
            print("IP地址检测失败")
    except Exception as e:
        print(f'[BUG]{type(e).__name__}:',e)

class Jmcomic():
    def __init__(self,username='',password='',cookies=None,session=None):
        self.__username = username
        self.__password = password
        self.session = session or requests.Session()
        print(f'初始化请求头:{self.session.headers}\n初始化Cookies:{self.session.cookies}')
        self.cookies = self.login()

    # 选择分流
    def shunt(self):
        return ['https://18comic.vip']

    # 登录
    def login(self):
        get_shunt = self.shunt()
        self.shunt_url = get_shunt[0]
        print('当前请求分流 --> ' + self.shunt_url)
        headers = {
            "origin": self.shunt_url,
            "referer": self.shunt_url,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
            'Connection':'close'
        }
        url = self.shunt_url + "/login"
        data = {
            "username": self.__username,
            "password": self.__password,
            "submit_login": "1"
        }
        response = self.session.post(url, headers=headers, data=data)
        if DEBUG: print('登录响应:', response.text)
        cookies = response.cookies.get_dict()
        if DEBUG: print('Cookies:\n',cookies)
        return cookies

    # 签到 + 10Exp + 5Gold
    def check_in(self):
        url = self.shunt_url + "/ajax/user_daily_sign"
        data = {
            "daily_id": "47",
            "oldStep": "1"
        }
        response = self.session.post(url, data=data).json()
        print(response)

    # 广告 + 5Exp(2) + 5Gold(5)
    def ad_check(self):  
        g = 0
        e = 0
        while True:
            response = self.session.get(self.shunt_url + "/ajax/ad_check" )
            msg = response.json()['msg']
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
        # print(f'已完成每日廣告點擊: 獲得「30」金幣、「10」經驗值')
        print(f'已完成每日廣告點擊: 獲得「{g}」金幣、「{e}」經驗值')

    # 喜欢作品 + 5Exp 存在漏洞(取消album_id、referer，再次正常请求)
    def like_check(self):
        url = self.shunt_url + "/ajax/vote_album"
        for i in range(4):
            data = {
                "album_id": str(313827+i), # ComicID
                "vote": "likes"
            }
            response = self.session.post(url, data=data)
            if DEBUG: print(response.json())
            print(f'ID {313827+i}: {response.json()["msg"]}')

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
    username = ''
    password = ''
    cookies = None
    Jmcomic(username,password,cookies).action()