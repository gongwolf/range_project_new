# %%
from datetime import date
from pathlib import Path
from sys import platform
import json
import pandas as pd

from GPSrecord import GPSrecord
from GPSrecord import processedFeedObj
from GPSrecord import processedPacketObj
from GPSrecord import resolvedTrackerObj
from GPSrecord import rawPositionObj

import io

import sys

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


def processRecord(data):
    # try:
    # print("{} : {} ".format(idx, record))
    coordinate = {
        "lng": data["coordinates"][0],
        "lat": data["coordinates"][1],
        "alt": data["coordinates"][2]
    }
    record_obj = GPSrecord(coordinate)
    record_obj.dxProfileId = data["dxProfileId"]
    record_obj.customerId = data["customerId"]
    record_obj.deviceEUI = data["deviceEUI"]
    record_obj.time = data["time"]
    record_obj.age = data["age"]
    record_obj.validityState = data["validityState"]
    record_obj.horizontalAccuracy = data["horizontalAccuracy"]

    ##########################################################################
    p_feed_obj = processedFeedObj()
    p_feed_obj.SF = data["processedFeed"]["SF"] if "SF" in data["processedFeed"] else -99
    p_feed_obj.payloadEncoded = data["processedFeed"]["payloadEncoded"] if "payloadEncoded" in data[
        "processedFeed"] else ''
    p_feed_obj.sequenceNumber = data["processedFeed"]["sequenceNumber"] if "sequenceNumber" in data[
        "processedFeed"] else -99
    if "dynamicMotionState" in data["processedFeed"]:
        p_feed_obj.dynamicMotionState = data["processedFeed"]["dynamicMotionState"]
    if "temperatureMeasure" in data["processedFeed"]:
        p_feed_obj.temperatureMeasure = data["processedFeed"]["temperatureMeasure"]

    p_packet_obj = processedPacketObj({})
    p_packet_obj.SNR = data["processedFeed"]["processedPacket"]["SNR"] if "SNR" in data["processedFeed"][
        "processedPacket"] else -99
    if "RSSI" in data["processedFeed"]["processedPacket"]:
        p_packet_obj.RSSI = data["processedFeed"]["processedPacket"]["RSSI"]
    if "baseStationId" in data["processedFeed"]["processedPacket"]:
        p_packet_obj.baseStationId = data["processedFeed"]["processedPacket"]["baseStationId"]
    if "antennaCoordinates" in data["processedFeed"]["processedPacket"]:
        p_packet_obj.antennaCoordinates = {
            "lng": data["processedFeed"]["processedPacket"]["antennaCoordinates"][0],
            "lat": data["processedFeed"]["processedPacket"]["antennaCoordinates"][1]
        }
    p_feed_obj.processedPacket = p_packet_obj

    ##########################################################################
    r_position_obj = rawPositionObj({})
    if "rawPosition" in data:
        r_position_obj.coordinates = {
            "lng": data["rawPosition"]["coordinates"][0],
            "lat": data["rawPosition"]["coordinates"][1],
            "alt": data["rawPosition"]["coordinates"][2]
        }
        r_position_obj.rawPositionType = data["rawPosition"]["rawPositionType"]

    ##########################################################################
    r_solved_obj = resolvedTrackerObj()
    r_solved_obj.firmwareVersion = data["resolvedTracker"]["firmwareVersion"]
    r_solved_obj.messageType = data["resolvedTracker"]["messageType"]
    r_solved_obj.trackingMode = data["resolvedTracker"]["trackingMode"]
    r_solved_obj.gpsScanMode = data["resolvedTracker"]["gpsScanMode"]
    r_solved_obj.sensorMode = data["resolvedTracker"]["sensorMode"]
    r_solved_obj.periodicPositionInterval = data["resolvedTracker"]["periodicPositionInterval"]
    r_solved_obj.batteryLevel = data["resolvedTracker"]["batteryLevel"]
    if "resolvedTracker" in data and "activityCount" in data["resolvedTracker"]:
        r_solved_obj.activityCount = data["resolvedTracker"]["activityCount"]

    ###########################################################################
    record_obj.processedFeed = p_feed_obj
    record_obj.rawPosition = r_position_obj
    record_obj.resolvedTracker = r_solved_obj
    return record_obj


# except:
#     error_folder = ''
#     if platform == "linux":
#         error_folder = './logs/error'
#     elif platform == "win32":
#         error_folder = 'Z:\logs\error'
#     error_p = Path(error_folder)
#     if not error_p.exists():
#         error_p.mkdir()
#
#     today_error_log_file = date.today().__str__().replace("-", "_") + "_error.log"
#     p_error_log_file =error_p/today_error_log_file
#     with p_error_log_file.open("a") as f:
#         e = sys.exc_info()
#         print("Error: {} ".format(e))
#         print("Error data : {}".format(data))
#         print("============================================")
#         f.write("Error: {} \n".format(e))
#         f.write("Error data : {}\n".format(data))
#         f.write("============================================\n")


def updateTheCSVFile(str_log_file_name, record):
    log_folder = ''
    if platform == "linux":
        log_folder = './logs/csv'
    elif platform == "win32":
        log_folder = 'Z:\logs\csv'
    p = Path(log_folder)
    if not p.exists():
        p.mkdir()
    str_file_name = str_log_file_name + ".csv"
    csv_p = p / str_file_name

    json_record = ""
    if type(record) is str:
        json_record = json.loads(record)
    else:
        json_record = record

    if not csv_p.exists():
        with csv_p.open("a") as f:
            obj_data = processRecord(json_record)
            headers = obj_data.getHeaderList()
            str_header = ",".join(headers)
            f.write(str_header)
            f.write("\n")
            f.write(obj_data.to_CSV_str())
    else:
        obj_data = processRecord(json_record)
        headers = obj_data.getHeaderList()
        csv_df = pd.read_csv(csv_p, header=0)
        new_row = pd.Series(obj_data.to_CSV_str().split(","), index=csv_df.columns)
        new_df = csv_df.append(new_row, ignore_index=True)
        csv_p.unlink()
        # print(new_df.head())
        new_df.sort_values(['deviceEUI', 'time'], ascending=[True, True])
        new_df.to_csv(csv_p, index=None)


def writeToDisk(json_data):
    log_folder = ""
    if platform == "linux":
        log_folder = './logs'
    elif platform == "win32":
        log_folder = "Z:\logs"

    p = Path(log_folder)
    if not p.exists():
        p.mkdir()
    today_log_file = date.today().__str__().replace("-", "_") + "_gps.log"
    log_p = p / today_log_file
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

    str_today = date.today().__str__().replace("-", "_")
    updateTheCSVFile(str_today, json_data)


# writeToDisk(json_data)
