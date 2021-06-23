import requests


def updateParameters(target_url, data):
    # url = 'https://dx-api.thingpark.com/location-trackercommand/latest/api/trackerCommands'

    header = {}
    header.update({'Content-Type': 'application/x-www-form-urlencoded'})
    header.update({'Accept': 'application/json'})
    header.update({
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjQ1MTk0Il0sImV4cCI6MTYyNDEyNTAwMiwianRpIjoiMzA2OTc3OGItZWJiNC00MGMwLWJjYWQtYWVmMDk5Zjk1MzQyIiwiY2xpZW50X2lkIjoidHBlLWV1LWFwaS9xaXh1Z29uZ0BubXN1LmVkdSJ9.ljwZ7lNmunGmubspNn4DSGnfQSBjZYB23ifR4jU6-8bZqM_hEDfZBNJPWEc7vdsyDK8oG9Xl0dhvNcf2bTnyNA'})

    req = requests.post(target_url, data=data, headers=header)
    # print(req.content)
    return req.text


if __name__ == "__main__":
    data="grant_type=client_credentials&client_id=tpe-eu-api%2Fqixugong%40nmsu.edu&client_secret=KKpdFU6YjQTeDdT"
    target_url = "https://dx-api.thingpark.com/admin/latest/api/oauth/token?renewToken=false&validityPeriod=7days"
    print(updateParameters(target_url, data))


