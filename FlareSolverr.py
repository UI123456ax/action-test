import requests
import os
import Script

url = "http://localhost:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
    "cmd": "request.get",
    # "url": "https://ip.sb/",
    "url": "https://18comic.vip/",
    "maxTimeout": 160000
}

response = requests.post(url, headers=headers, json=data)
print("Status:", response.json().get('status', {}))
print("Status Code:", response.status_code)
print("FlareSolverr message:", response.json().get('message', {}))

cookies = {}
if response.status_code == 200:
    print(response.json()['solution']['response'][:300])
    for item in response.json()['solution']['cookies']:
        cookies[item["name"]] = item["value"]
    userAgent = response.json()['solution']['userAgent']

def cf_request(cookies, userAgent):
    session = requests.session()
    session.headers.update({"User-Agent": userAgent})
    session.cookies.update(cookies)
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    Script.Jmcomic(username=username, password=password, session=session).action()

if __name__ == '__main__':
    cf_request(cookies, userAgent)