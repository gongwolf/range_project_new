# %%
from datetime import date
from pathlib import Path
import json

# json_data = """
# {
#   "dxProfileId": "iot-api",
#   "customerId": "100033601",
#   "deviceEUI": "20635F00C8000015",
#   "time": "2019-10-10T21:44:03.311000+00:00",
#   "coordinates": [
#     -106.80398,
#     32.529972,
#     0.0
#   ],
#   "age": 188961,
#   "validityState": "PREVIOUS",
#   "horizontalAccuracy": 7,
#   "processedFeed": {
#     "payloadEncoded": "03489499a0251370fec0608e01dca206",
#     "sequenceNumber": 13895,
#     "dynamicMotionState": "STATIC",
#     "temperatureMeasure": 33.4,
#     "processedPacket": {
#       "RSSI": -45.0,
#       "baseStationId": "08080056",
#       "antennaCoordinates": [
#         -106.74136,
#         32.61721
#       ]
#     }
#   },
#   "rawPosition": {
#     "rawPositionType": "RawPositionByGpsSolver",
#     "coordinates": [
#       -106.7414,
#       32.617214,
#       0.0
#     ]
#   },
#   "resolvedTracker": {
#     "firmwareVersion": "1.7.3",
#     "messageType": "Position Message",
#     "trackingMode": "PERMANENT_TRACKING",
#     "gpsScanMode": "UNKNOWN",
#     "sensorMode": "GPS_ONLY",
#     "periodicPositionInterval": 0,
#     "batteryLevel": 68,
#     "activityCount": -1
#   }
# }"""

# %%


def writeToDisk(json_data):
    log_folder = "Z:\logs"
    p = Path(log_folder)
    if not p.exists():
        p.mkdir()
    today_log_file = date.today().__str__().replace("-", "_")+"_gps.log"
    log_p = p/today_log_file
    # print(log_p.exists())
    if not log_p.exists():
        # print("The log file does not exist, create it")
        with open(log_p, 'w') as f:
            f.write("[")
            f.write(json_data)
            f.write("]")
    else:
        # print("The log file exists, open it")
        json_file = open(log_p, 'r')
        data = json.load(json_file)
        json_file.close()
        data.append(json.loads(json_data))
        with open(log_p, 'w') as f:
            json.dump(data, f)


# %%
# writeToDisk(json_data)
# %%
