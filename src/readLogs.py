from os import listdir
from os.path import isfile, join
import json


logs_file_folder = "src/logs"

# get the list of the log files
log_files = [f for f in listdir(
    logs_file_folder) if isfile(join(logs_file_folder, f))]

# read the log file one by one
list_of_devices = set()
for log_file in log_files:
    log = "{}/{}".format(logs_file_folder, log_file)
    print(log)
    with open(log) as f:
        data = json.load(f)

    id = 1
    for record in data:
        device_id = record["deviceEUI"]
        print(id, " : ", device_id, " ---- ", record["time"])
        list_of_devices.add(device_id)
        id += 1

print(list_of_devices)
print(len(list_of_devices))