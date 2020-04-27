import json
from os import listdir
from os.path import isfile, join, split, basename
import sys

from GPSrecord import GPSrecord
from GPSrecord import processedFeedObj
from GPSrecord import processedPacketObj
from GPSrecord import resolvedTrackerObj
from GPSrecord import rawPositionObj

path = "/home/gqxwolf/google-drive/Cibils_Project/log"

log_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def sortbylogfiledate(filename):
    return basename(filename)


log_files.sort(key=sortbylogfiledate)

def read_Json(f):
    gps_records = []
    # print("Process the log file : {} ".format(f))
    with open(f, "r") as read_file:
        data = json.load(read_file)
        for idx, record in enumerate(data, start=1):
            try:
                # print("{} : {} ".format(idx, record))
                coordinate = {
                    "lng": record["coordinates"][0],
                    "lat": record["coordinates"][1],
                    "alt": record["coordinates"][2]
                }
                record_obj = GPSrecord(coordinate)
                record_obj.dxProfileId = record["dxProfileId"]
                record_obj.customerId = record["customerId"]
                record_obj.deviceEUI = record["deviceEUI"]
                record_obj.time = record["time"]
                record_obj.age = record["age"]
                record_obj.validityState = record["validityState"]
                record_obj.horizontalAccuracy = record["horizontalAccuracy"]

                ##########################################################################
                p_feed_obj = processedFeedObj()
                p_feed_obj.SF = record["processedFeed"]["SF"]
                p_feed_obj.payloadEncoded = record["processedFeed"]["payloadEncoded"]
                p_feed_obj.sequenceNumber = record["processedFeed"]["sequenceNumber"]
                p_feed_obj.dynamicMotionState = record["processedFeed"]["dynamicMotionState"]
                p_feed_obj.temperatureMeasure = record["processedFeed"]["temperatureMeasure"]

                p_packet_obj = processedPacketObj({})
                p_packet_obj.SNR = record["processedFeed"]["processedPacket"]["SNR"]
                p_packet_obj.RSSI = record["processedFeed"]["processedPacket"]["RSSI"]
                p_packet_obj.baseStationId = record["processedFeed"]["processedPacket"]["baseStationId"]
                p_packet_obj.antennaCoordinates = {
                    "lng": record["processedFeed"]["processedPacket"]["antennaCoordinates"][0],
                    "lat": record["processedFeed"]["processedPacket"]["antennaCoordinates"][1]
                }
                p_feed_obj.processedPacket = p_packet_obj

                ##########################################################################
                r_position_obj = rawPositionObj({})
                if "rawPosition" in record:
                    r_position_obj.coordinates = {
                        "lng": record["rawPosition"]["coordinates"][0],
                        "lat": record["rawPosition"]["coordinates"][1],
                        "alt": record["rawPosition"]["coordinates"][2]
                    }
                    r_position_obj.rawPositionType = record["rawPosition"]["rawPositionType"]

                ##########################################################################
                r_solved_obj = resolvedTrackerObj()
                r_solved_obj.firmwareVersion = record["resolvedTracker"]["firmwareVersion"]
                r_solved_obj.messageType = record["resolvedTracker"]["messageType"]
                r_solved_obj.trackingMode = record["resolvedTracker"]["trackingMode"]
                r_solved_obj.gpsScanMode = record["resolvedTracker"]["gpsScanMode"]
                r_solved_obj.sensorMode = record["resolvedTracker"]["sensorMode"]
                r_solved_obj.periodicPositionInterval = record["resolvedTracker"]["periodicPositionInterval"]
                r_solved_obj.batteryLevel = record["resolvedTracker"]["batteryLevel"]
                if "resolvedTracker" in record and "activityCount" in record["resolvedTracker"]:
                    r_solved_obj.activityCount = record["resolvedTracker"]["activityCount"]

                ###########################################################################
                # Assign to GPS object
                record_obj.processedFeed = p_feed_obj
                record_obj.rawPosition = r_position_obj
                record_obj.resolvedTracker = r_solved_obj
                # if record_obj.deviceEUI == "20635F00C8000015":
                # print("{} : {}".format(idx,record_obj))
                gps_records.append(record_obj)
            except:
                e = sys.exc_info()
                print("Error: {} ".format(e))
                print("{} : {}".format(idx, record))
                print("============================================")

    return gps_records


for f in log_files:
    # if f.__contains__("2020_03_20_gps.log"):
    gps_records = read_Json(f)
    print("process the file {} that is contains {} records ".format(f, len(gps_records)))
    # break
