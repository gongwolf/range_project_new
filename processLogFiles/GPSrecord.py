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
