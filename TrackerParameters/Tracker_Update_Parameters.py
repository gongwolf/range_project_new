import requests
from sys import platform
from os.path import isfile, join

# data = """
# {
#   "trackerCommandType": "TrackerCommandToChangeParams",
#   "deviceEUI": "20635F00C80000E4",
#   "status": "QUEUED",
#   "parameters":
#               [
#                {"paramName":"GEOLOC_SENSOR_PROFILE", "paramValue":1},
#                {"paramName":"ONESHOT_GEOLOC_METHOD", "paramValue":1}
#               ]
#
#
# }
# """

# {'trackerCommandType': 'TrackerCommandToChangeParams',
#  'deviceEUI': '20635F00C8000062',
#  'status': 'QUEUED',
#  'parameters':[
#      {'paramName':'GEOLOC_SENSOR_PROFILE', 'paramValue':1},
#      {'paramName':'ONESHOT_GEOLOC_METHOD', 'paramValue':1}
#  ]
#  }



if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = "C:\\range_project_new"

if platform == "linux":
    path = "/home/gqxwolf/mydata/range_project_new/logs"
elif platform == "win32":
    path = "Z:\\logs"
    device_data_file = home_folder + "\\data\\DeviceList"

device_data_file = join(home_folder, "data", "DeviceList")


def updateParameters(data):
    url = 'https://dx-api.thingpark.com/location-trackercommand/latest/api/trackerCommands'

    header = {}
    header.update({'Content-Type': 'application/json'})
    header.update({'accept': 'application/json'})
    header.update({
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjMzNjAxIl0sImV4cCI6MTYwMjM5MjQ5OSwianRpIjoiZWIwNDJhOTctNTYxMi00ODg5LTg3ZjktODJmMGM2N2Y0YzEzIiwiY2xpZW50X2lkIjoiaW90LWFwaS9hY2liaWxzQG5tc3UuZWR1In0.O0qpLFoUTN96I6Ut5RVg-qbXaIWNuJ99SyZ9V21jT5BO99y-A9BmysIW7YyoZHhOIksZZtVP3wD2RSdPw8WtBg'})

    req = requests.post(url, data=data, headers=header)
    # print(req.content)
    return req.status_code


if __name__ == "__main__":
    with open(device_data_file) as f:
        device_list = f.readlines()
        device_list = [str(d.strip()) for d in device_list]
        for index, d in enumerate(device_list, 1):
            data = "{\"trackerCommandType\": \"TrackerCommandToChangeParams\",\"deviceEUI\": \"" + d + "\",\"status\": \"QUEUED\",\"parameters\":[{\"paramName\":\"GEOLOC_SENSOR_PROFILE\", \"paramValue\":1},{\"paramName\":\"ONESHOT_GEOLOC_METHOD\", \"paramValue\":1}]}"
            # print(data)
            status_code = updateParameters(data)
            print("{}: device: {}   --> status_code:{}".format(index, d, status_code))
