import requests


def updateParameters(target_url, data):
    # url = 'https://dx-api.thingpark.com/location-trackercommand/latest/api/trackerCommands'

    header = {}
    header.update({'Content-Type': 'application/x-www-form-urlencoded'})
    header.update({'Accept': 'application/json'})
    header.update({
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjQ1MTk0Il0sImV4cCI6MTYyMzI4MTI5NSwianRpIjoiYWQxMmM2ZjktNGE3Mi00ZTJjLThmYmMtOWYwOWVjY2RmZGFmIiwiY2xpZW50X2lkIjoidHBlLWV1LWFwaS9xaXh1Z29uZ0BubXN1LmVkdSJ9.Rjxzf3UH39oXq-AYBjmU5TMdnAylf4hdN7kceoenEB3KyavYldlQIaRTXoz65sU4W-nk9As6YAbW3Yjc2NgrZg","scope":"[SUBSCRIBER:45194]","jti":"ad12c6f9-4a72-4e2c-8fbc-9f09eccdfdaf'})

    req = requests.post(target_url, data=data, headers=header)
    # print(req.content)
    return req.text


if __name__ == "__main__":
    data="grant_type=client_credentials&client_id=tpe-eu-api%2Fqixugong%40nmsu.edu&client_secret=KKpdFU6YjQTeDdT"
    target_url = "https://dx-api.thingpark.com/admin/latest/api/oauth/token?renewToken=false&validityPeriod=7days"
    print(updateParameters(target_url, data))


