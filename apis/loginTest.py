import requests

# This URL will be the URL that your login form points to with the "action" tag.
POST_LOGIN_URL = 'https://iot.thingpark.com/thingpark/smp/login?applicationID=actility-sup/abeeway-device-analyzer'

# This URL is the page you actually want to pull down with requests.
REQUEST_URL = 'https://iot.thingpark.com/abeewayDeviceAnalyzer/selecttracker.php'

payload = {
    'login': 'acibils@nmsu.edu',
    'password': 'LTARlora2020',
    'uri':'/thingpark/smp/rest/applications/5470',
    'application':'Abeeway Device Analyzer',
    'applicationID':'actility-sup/abeeway-device-analyzer',
    'gmaps':''
}

with requests.Session() as session:
    post = session.post(POST_LOGIN_URL, data=payload)
    # print(post.text)
    r = session.get(REQUEST_URL)
    print(r.text)   #or whatever else you want to do with the request data!