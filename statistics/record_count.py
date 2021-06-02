import time
from datetime import datetime, timedelta
from sys import platform
from os.path import isfile, join
from os import listdir
from pathlib import Path
from typing import List
import schedule
import sys
import numpy as np

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = "C:\\range_project_new"

sys.path.append(home_folder)

import tools.gps_tools

if platform == "linux":
    path = "/home/gqxwolf/mydata/range_project_new/logs"
elif platform == "win32":
    path = "Z:\\logs"
    device_data_file = home_folder + "\\data\\DeviceList"

device_data_file = join(home_folder, "data", "DeviceList")

with open(device_data_file) as f:
    device_list = f.readlines()
    device_list = [d.strip() for d in device_list]


def record_quality_count(gps_records):
    count_list = {k: [] for k in device_list}
    result = {k: {"total": 0, "bad": 0, "new": 0} for k in device_list}
    result["Overall"] = {"total": 0, "bad": 0, "new": 0}
    for record in gps_records:
        device_id = record.deviceEUI.upper()
        vadility = record.validityState

        if device_id not in device_list:
            continue

        result[device_id]["total"] += 1
        result["Overall"]["total"] += 1
        if vadility == "NEW":
            result[device_id]["new"] += 1
            result["Overall"]["new"] += 1
        elif vadility == "PREVIOUS" or vadility == "INVALID":
            result[device_id]["bad"] += 1
            result["Overall"]["bad"] += 1
        count_list[device_id].append(record.processedFeed.sequenceNumber)

    lost_pac_result = {k: {"num": 0, "ratio": 0.0} for k in device_list}
    lost_pac_result["Overall"] = {"num": 0, "ratio": 0.0}

    total_expect_num = 0
    total_lost_num = 0

    for dev in count_list:
        if len(count_list[dev]) != 0:
            seq_list = np.asarray(count_list[dev])
            expect_num = (seq_list.max() - seq_list.min() + 1);
            act_num = len(seq_list)
            lost_pac_result[dev]["ratio"] = round((expect_num - act_num) / expect_num, 5) * 100
            lost_pac_result[dev]["num"] = (expect_num - act_num)
            total_expect_num += expect_num
            total_lost_num += (expect_num - act_num)
            # print(dev, seq_list.max(), seq_list.min(), seq_list.max() - seq_list.min(), len(seq_list), lost_pac_result[dev]["ratio"] , lost_pac_result[dev]["num"])

        else:
            # print(dev, 0, 0, 0, 0)
            lost_pac_result[dev]["ratio"] = 0.0
            lost_pac_result[dev]["num"] = 0

    # print(lost_pac_result)
    lost_pac_result["Overall"]["ratio"] = round(total_lost_num / total_expect_num, 5) * 100
    lost_pac_result["Overall"]["num"] = total_lost_num
    return result, lost_pac_result


def process_log_files_quality_count(log_files):
    result: List[str] = []
    if platform == "linux":
        log_folder = home_folder + "/logs/statistics/record_quality"
    elif platform == "win32":
        log_folder = "Z:\logs\statistics\\record_quality"
    p = Path(log_folder)
    if not p.exists():
        p.mkdir(parents=True)

    for f in log_files:
        # print(f)
        log_p = Path(f)
        year = log_p.stem.split("_")[0]
        month = log_p.stem.split("_")[1]
        day = log_p.stem.split("_")[2]

        gps_records = tools.gps_tools.read_Json(f)
        (counts_results, lost_pac_result) = record_quality_count(gps_records)
        str_re = "In the file {}, there are {} records are found ".format(
            f, len(gps_records)
        )
        print(str_re)
        result.append(str_re)

        file_name = "record_statistics_" + year + "_" + month + "_" + day + ".csv"

        file_p = p / file_name
        if file_p.exists():
            file_p.unlink()

        with open(file_p, "w") as f:
            header = (
                "Device_id, total # of records, # of good records, # of bad records, # of the lost packages, lost ratio(%)\n"
            )
            f.write(header)
            for key, value in counts_results.items():
                f.write(
                    "{},{},{},{},{},{}\n".format(
                        key, value["total"], value["new"], value["bad"], lost_pac_result[key]["num"],
                        lost_pac_result[key]["ratio"]
                    )
                )
        # sys.exit()

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    str_re = "{} : ================================================================".format(
        dt_string
    )
    print(str_re)
    result.append(str_re)
    return result


def record_count_with_date(date):
    try:
        print("Call refresh function with parameters [{}] !!!!!!".format(date))
        print("There are total {} devices.".format(len(device_list)))
        log_files = [
            join(path, f)
            for f in listdir(path)
            if isfile(join(path, f)) and f.__contains__(date)
        ]
        result = process_log_files_quality_count(log_files)
        return result
    except:
        now = datetime.now()
        str_datetime = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("call the function record_count_with_date() error at {}".format(str_datetime))



def record_count():
    try:
        print("Call refresh function without parameters !!!!!!")
        print("There are total {} devices.".format(len(device_list)))
        log_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        result = process_log_files_quality_count(log_files)
        return result
    except:
        now = datetime.now()
        str_datetime = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("call the function record_count() error at {}".format(str_datetime))


def record_count_with_today():
    today = datetime.now().strftime("%Y_%m_%d")
    record_count_with_date(today)


def record_count_with_yesterday():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y_%m_%d")
    record_count_with_date(yesterday)


if __name__ == "__main__":
    # record_count_with_date("2020_04_20")
    # today = datetime.now().strftime("%Y_%m_%d")
    # yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y_%m_%d")
    print("Running the script of calculating the quality of the records:-------------------------")
    print("======================================================================================")
    schedule.every().day.at("00:10").do(record_count_with_today)
    schedule.every().day.at("00:10").do(record_count_with_yesterday)

    schedule.every().day.at("06:00").do(record_count_with_today)
    schedule.every().day.at("12:00").do(record_count_with_today)
    schedule.every().day.at("18:00").do(record_count_with_today)
    schedule.every().day.at("23:00").do(record_count_with_today)

    # schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(60)
