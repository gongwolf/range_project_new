import json
from os import listdir
from os.path import isfile, join, basename

from tools.GPSrecord import GPSrecord
from tools.GPSrecord import processedFeedObj
from tools.GPSrecord import processedPacketObj
from tools.GPSrecord import resolvedTrackerObj
from tools.GPSrecord import rawPositionObj

from sys import platform
from pathlib import Path
import pandas as pd

if platform == "linux":
    path = "/home/gqxwolf/google-drive/Cibils_Project/log"
elif platform == "win32":
    path = 'Z:\logs'

log_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def sortbylogfiledate(filename):
    return basename(filename)


log_files.sort(key=sortbylogfiledate)


def read_Json(f):
    gps_records = []
    # print("Process the log file : {} ".format(f))
    with open(f, "r") as read_file:
        records = json.load(read_file)
        for idx, data in enumerate(records, start=1):
            # try:
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
            r_position_obj = rawPositionObj({"lng": -9999, "lat": -9999, "alt": -9999})
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
            gps_records.append(record_obj)
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
        #     p_error_log_file = error_p / today_error_log_file
        #     with p_error_log_file.open("a") as f:
        #         e = sys.exc_info()
        #         print("Error: {} ".format(e))
        #         print("Error data : {}".format(data))
        #         print("============================================")
        #         f.write("Error: {} \n".format(e))
        #         f.write("Error data : {}\n".format(data))
        #         f.write("============================================\n")

    return gps_records

for f in log_files:
    # if f.__contains__("2020_03_20_gps.log"):
    # gps_records = read_Json(f)
    # print("process the file {} that is contains {} records ".format(f, len(gps_records)))
    # print(gps_records[0].tojson())

    if platform == "linux":
        log_folder = './logs/csv'
    elif platform == "win32":
        log_folder = 'Z:\logs\csv'
    p = Path(log_folder)
    if not p.exists():
        p.mkdir()

    log_p = Path(f)
    year = log_p.stem.split("_")[0]
    month = log_p.stem.split("_")[1]
    day = log_p.stem.split("_")[2]

    str_file_name = year + "_" + month + "_" + day + ".csv"
    csv_p = p / str_file_name

    if csv_p.exists():
        csv_p.unlink()

    gps_records = read_Json(f)
    if len(gps_records) is not 0:
        headers = gps_records[0].getHeaderList()
        csv_df = pd.DataFrame(columns=headers)
        for obj_data in gps_records:
            new_row = pd.Series(obj_data.to_CSV_str().split(","), index=csv_df.columns)
            csv_df = csv_df.append(new_row, ignore_index=True)

        csv_df = csv_df.sort_values(['deviceEUI', 'time'], ascending=[True, True])
        csv_df.drop_duplicates(keep='first', inplace=True)
        csv_df.to_csv(csv_p, index=None)

        print("{} {} ".format(f, csv_df.shape))
