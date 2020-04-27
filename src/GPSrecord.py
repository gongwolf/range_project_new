from dataclasses import dataclass
import json


@dataclass
class processedPacketObj:
    antennaCoordinates: dict
    SNR: float = -99
    RSSI: float = -99
    baseStationId: str = ""


@dataclass
class rawPositionObj:
    coordinates: dict
    rawPositionType: str = ""


@dataclass
class resolvedTrackerObj:
    firmwareVersion: str = ""
    messageType: str = ""
    trackingMode: str = ""
    gpsScanMode: str = ""
    sensorMode: str = ""
    periodicPositionInterval: int = -99
    batteryLevel: int = -99
    activityCount: int = -99


@dataclass
class processedFeedObj:
    SF: int = -99
    payloadEncoded: str = ""
    sequenceNumber: int = -99
    dynamicMotionState: str = ""
    temperatureMeasure: float = -99
    processedPacket: processedPacketObj = processedPacketObj({})


@dataclass
class GPSrecord:
    coordinates: dict
    dxProfileId: str = ""
    customerId: str = ""
    deviceEUI: str = ""
    time: str = ""
    age: str = ""
    validityState: str = ""
    horizontalAccuracy: int = -99
    processedFeed: processedFeedObj = processedFeedObj()
    rawPosition: rawPositionObj = rawPositionObj({})
    resolvedTracker: resolvedTrackerObj = resolvedTrackerObj()

    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_CSV_str(self):
        """
            TODO:check the field has value
            Do not need to consider the null value, each field has default value
        """
        res_str = ''
        res_str += self.dxProfileId + ","
        res_str += self.customerId + ","
        res_str += self.deviceEUI + ","
        res_str += self.time + ","
        res_str += str(self.coordinates["lng"]) + ","
        res_str += str(self.coordinates["lat"]) + ","
        res_str += str(self.coordinates["alt"]) + ","
        res_str += str(self.age) + ","
        res_str += self.validityState + ","
        res_str += str(self.horizontalAccuracy) + ","
        ######################################################
        res_str += str(self.processedFeed.SF) + ","
        res_str += self.processedFeed.payloadEncoded + ","
        res_str += str(self.processedFeed.sequenceNumber) + ","
        res_str += self.processedFeed.dynamicMotionState + ","
        res_str += str(self.processedFeed.temperatureMeasure) + ","
        ######################################################
        res_str += str(self.processedFeed.processedPacket.SNR) + ","
        res_str += str(self.processedFeed.processedPacket.RSSI) + ","
        res_str += self.processedFeed.processedPacket.baseStationId + ","
        res_str += str(self.processedFeed.processedPacket.antennaCoordinates["lng"]) + ","
        res_str += str(self.processedFeed.processedPacket.antennaCoordinates["lat"]) + ","
        ######################################################
        res_str += str(self.rawPosition.coordinates["lng"]) + ","
        res_str += str(self.rawPosition.coordinates["lat"]) + ","
        res_str += str(self.rawPosition.coordinates["alt"]) + ","
        res_str += self.rawPosition.rawPositionType + ","
        ######################################################
        res_str += self.resolvedTracker.firmwareVersion + ","
        res_str += self.resolvedTracker.messageType + ","
        res_str += self.resolvedTracker.trackingMode + ","
        res_str += self.resolvedTracker.gpsScanMode + ","
        res_str += self.resolvedTracker.sensorMode + ","
        res_str += str(self.resolvedTracker.periodicPositionInterval) + ","
        res_str += str(self.resolvedTracker.batteryLevel) + ","
        res_str += str(self.resolvedTracker.activityCount)
        return res_str

    def getHeaderList(self):
        header=[]
        header.append("dxProfileId")
        header.append("customerId")
        header.append("deviceEUI")
        header.append("time")
        header.append("coordinates.lng")
        header.append("coordinates.lat")
        header.append("coordinates.alt")
        header.append("age")
        header.append("validityState")
        header.append("horizontalAccuracy")
        ########################################
        header.append("processedFeed.SF")
        header.append("processedFeed.payloadEncoded")
        header.append("processedFeed.sequenceNumber")
        header.append("processedFeed.dynamicMotionState")
        header.append("processedFeed.temperatureMeasure")
        ########################################
        header.append("processedFeed.processedPacket.SNR")
        header.append("processedFeed.processedPacket.RSSI")
        header.append("processedFeed.processedPacket.baseStationId")
        header.append("processedFeed.processedPacket.antennaCoordinates.lng")
        header.append("processedFeed.processedPacket.antennaCoordinates.lat")
        ########################################
        header.append("rawPosition.coordinates.lng")
        header.append("rawPosition.coordinates.lat")
        header.append("rawPosition.coordinates.alt")
        header.append("rawPosition.rawPositionType")
        ########################################
        header.append("resolvedTracker.firmwareVersion")
        header.append("resolvedTracker.messageType")
        header.append("resolvedTracker.trackingMode")
        header.append("resolvedTracker.gpsScanMode")
        header.append("resolvedTracker.sensorMode")
        header.append("resolvedTracker.periodicPositionInterval")
        header.append("resolvedTracker.batteryLevel")
        header.append("resolvedTracker.activityCount")

        return header

