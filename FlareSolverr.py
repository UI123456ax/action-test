import requests

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
    print(response.json())
    for item in response.json()['solution']['cookies']:
        cookies[item["name"]] = item["value"]
    userAgent = response.json()['solution']['userAgent']