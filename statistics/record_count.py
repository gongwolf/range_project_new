import sys
from sys import platform
from os.path import isfile, join, basename
from os import listdir
from pathlib import Path
import tools.gps_tools
import schedule

if platform == "linux":
    path = "/home/gqxwolf/google-drive/Cibils_Project/log"
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    path = 'Z:\logs'

with open(home_folder + "/data/DeviceList") as f:
    device_list = f.readlines()
    device_list = [d.strip() for d in device_list]


def record_quality_count(gps_records):
    result = {k: {"total": 0, "bad": 0, "new": 0} for k in device_list}
    result['Overall'] = {"total": 0, "bad": 0, "new": 0}
    for record in gps_records:
        device_id = record.deviceEUI
        vadility = record.validityState
        result[device_id]["total"] += 1
        result['Overall']["total"] += 1
        if vadility == "NEW":
            result[device_id]["new"] += 1
            result['Overall']["new"] += 1
        elif vadility == "PREVIOUS" or vadility == "INVALID":
            result[device_id]["bad"] += 1
            result['Overall']["bad"] += 1

    # for key, value in result.items():
    #     print("{} {}".format(key, value))
    return result


def main():
    print("There are total {} devices.".format(len(device_list)))

    log_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    if platform == "linux":
        log_folder = home_folder + '/logs/statistics'
    elif platform == "win32":
        log_folder = 'Z:\logs\statistics'
    p = Path(log_folder)
    if not p.exists():
        p.mkdir(parents=True)

    for f in log_files:
        log_p = Path(f)
        year = log_p.stem.split("_")[0]
        month = log_p.stem.split("_")[1]
        day = log_p.stem.split("_")[2]

        gps_records = tools.gps_tools.read_Json(f)
        counts_results = record_quality_count(gps_records)
        print("In the file {}, there are {} records are found ".format(f, len(gps_records)))

        file_name = "record_statistics_" + year + "_" + month + "_" + day + ".csv"

        file_p = p / file_name
        if file_p.exists():
            file_p.unlink()

        with open(file_p, "w") as f:
            header = "Device_id, total # of records, # of good records, # of bad records\n"
            f.write(header)
            for key, value in counts_results.items():
                f.write("{},{},{},{}\n".format(key, value['total'], value['bad'], value['new']))


if __name__ == "__main__":
    main()
