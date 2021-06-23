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

# data = """
# {
#   "deviceEUI": "20635F00C80000E4",
#   "trackerCommandType": "TrackerCommandToChangeMode",
#   "status": "QUEUED",
#   "newMode": "OFF"
# }
# """

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
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjQ1MTk0Il0sImV4cCI6MTYyNDEyNTAwMiwianRpIjoiMzA2OTc3OGItZWJiNC00MGMwLWJjYWQtYWVmMDk5Zjk1MzQyIiwiY2xpZW50X2lkIjoidHBlLWV1LWFwaS9xaXh1Z29uZ0BubXN1LmVkdSJ9.ljwZ7lNmunGmubspNn4DSGnfQSBjZYB23ifR4jU6-8bZqM_hEDfZBNJPWEc7vdsyDK8oG9Xl0dhvNcf2bTnyNA'})

    req = requests.post(url, data=data, headers=header)
    # print(req.content)
    return req.status_code


if __name__ == "__main__":
    with open(device_data_file) as f:
        device_list = f.readlines()
        device_list = [str(d.strip()) for d in device_list]
        for index, d in enumerate(device_list, 1):
            ##"Positioning Strategy" and "Periodic or On demand mode" be to changed to GPS only strategy.
            ##data = "{\"trackerCommandType\": \"TrackerCommandToChangeParams\",\"deviceEUI\": \"" + d + "\",\"status\": \"QUEUED\",\"parameters\":[{\"paramName\":\"GEOLOC_SENSOR_PROFILE\", \"paramValue\":1},{\"paramName\":\"ONESHOT_GEOLOC_METHOD\", \"paramValue\":1}]}"

            ## Change the tracker mode to OFF
            # data="{\"deviceEUI\": \"" + d + "\",\"trackerCommandType\": \"TrackerCommandToChangeMode\",\"status\": \"QUEUED\",\"newMode\": \"OFF\"}"

            # change the tracker mode to ACTIVITY_MONITORING
            # data="{\"deviceEUI\": \"" + d + "\",\"trackerCommandType\": \"TrackerCommandToSendRawData\",\"status\": \"QUEUED\",\"rawPayload\": \"020a04\"}"
            # print(data)
            # status_code = updateParameters(data)
            # print("{}: device: {}   --> status_code:{}".format(index, d, status_code))


            ## change the configuration
            #  UL_PERIOD = 60
            #  LORA_PERIOD = 300
            #  PERIODIC_POS_PERIOD = 900
            #  GEOLOC_SENSOR = 1
            #  GEOLOC_METHOD = 1
            # data="{\"deviceEUI\": \"" + d + "\",\"trackerCommandType\": \"TrackerCommandToSendRawData\",\"status\": \"QUEUED\",\"rawPayload\": \"0b0a000000003c0100000258030000038405000000010600000001\"}"
            # print(data)
            # status_code = updateParameters(data)
            # print("{}: device: {}   --> status_code:{}".format(index, d, status_code))
            # break

            # ## Change the transmission to "Double Random Datarate"
            data="{\"deviceEUI\": \"" + d + "\",\"trackerCommandType\": \"TrackerCommandToSendRawData\",\"status\": \"QUEUED\",\"rawPayload\": \"0b0a0e00000003\"}"
            print(data)
            status_code = updateParameters(data)
            print("{}: device: {}   --> status_code:{}".format(index, d, status_code))

