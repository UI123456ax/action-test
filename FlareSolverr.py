import cloudscraper


scraper = cloudscraper.create_scraper()
resp = scraper.get('https://18comic.vip').text
print(resp[:1000])  # Print the first 1000 characters of the response

import json
import requests

def cloudflare(self, xxxx):
    print("破盾中...")
    urlServer = "https://yadtenumogxm.eu-central-1.clawcloudrun.com/v1"
    payload = json.dumps({
        "cmd": "request.get",
        "url": 'https://18comic.vip',
        "maxTimeout": 160000
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(urlServer, headers=headers, data=payload)
    # print(response.status_code)
    # print(response.json()['solution']['cookies'])
    if response.status_code == 200:
        userAgent = response.json()['solution']['userAgent']
        for item in response.json()['solution']['cookies']:
            self.cookies[item["name"]] = item["value"]
        self.UA = userAgent
        print("破盾成功")
        return response
    print("绕过5秒盾错误！！！")