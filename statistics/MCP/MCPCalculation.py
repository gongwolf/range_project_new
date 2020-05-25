import time
from datetime import datetime, timedelta
from sys import platform
from os.path import isfile, join
from os import listdir
from pathlib import Path
from typing import List

import schedule
from scipy.spatial import ConvexHull
import sys
import numpy as np
from pyproj import Proj
from shapely.geometry import shape, Polygon

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = "C:\\range_project_new"

sys.path.append(home_folder)

import tools.gps_tools

if platform == "linux":
    path = "/home/gqxwolf/google-drive/Cibils_Project/log"
elif platform == "win32":
    path = "Z:\\logs"
    device_data_file = home_folder + "\\data\\DeviceList"

device_data_file = join(home_folder, "data", "DeviceList")

with open(device_data_file) as f:
    device_list = f.readlines()
    device_list = [d.strip() for d in device_list]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        str = "[{},{}]".format(self.x, self.y)
        return str


def get_points_list_by_device_id(gps_records, device_id):
    points = []
    for g in gps_records:
        if g.deviceEUI == device_id:
            # x = g.coordinates['lng'] if g.coordinates['lng'] > 0 else -g.coordinates['lng']
            # y = g.coordinates['lat'] if g.coordinates['lat'] > 0 else -g.coordinates['lat']
            x = g.coordinates['lng']
            y = g.coordinates['lat']
            p = Point(x, y)
            points.append(p)
    return points


def process_gps_records(log_files):
    result: List[str] = []

    if platform == "linux":
        log_folder = home_folder + "/logs/statistics/MCP"
    elif platform == "win32":
        log_folder = "Z:\logs\statistics\MCP"
    p_path = Path(log_folder)
    if not p_path.exists():
        p_path.mkdir(parents=True)

    for f in log_files:
        log_p = Path(f)
        year = log_p.stem.split("_")[0]
        month = log_p.stem.split("_")[1]
        day = log_p.stem.split("_")[2]

        file_name = "record_mcp_" + year + "_" + month + "_" + day + ".csv"
        file_p = p_path / file_name
        if file_p.exists():
            file_p.unlink()

        with open(file_p, "a+") as target_f:
            header = (
                "Device_id, total # of points, # of convex points, convex area, list of convex points\n"
            )
            target_f.write(header)

        gps_records = tools.gps_tools.read_Json(f)

        for device_id in device_list:
            points = get_points_list_by_device_id(gps_records, device_id)

            p_list = []
            for p in points:
                p_list.append([p.x, p.y])
            points_array = np.array(p_list)

            h_list = []
            convex_area = 0

            if len(points_array) != 0:
                u = np.unique(points_array, axis=0)
                if u.shape[0] >= 3:
                    hull = ConvexHull(u)

                    # get convex hull points list
                    hx = []
                    hy = []
                    for v in hull.vertices:
                        hx.append(u[v][0])
                        hy.append(u[v][1])
                        h_list.append([u[v][0], u[v][1]])

                    # project
                    lon, lat = zip(*[u[hull.vertices, :]][0])
                    pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=39.0 +lon_0=-106.55")
                    x, y = pa(lon, lat)

                    # calculate the area
                    ob = [zip(x, y)]
                    convex_area = Polygon(ob[0], ob[1:]).area  # square meters
            # print("device_id:{} len of points:{} len of convex list:{} convex_area:{}".format(device_id, len(points),
            #                                                                                   len(h_list), convex_area))

            with open(file_p, "a+") as target_f:
                s = ""
                for h in h_list:
                    s += "[{}-{}]|".format(h[0], h[1])
                target_f.write("{},{},{},{},{}\n".format(device_id, len(points), len(h_list), convex_area, s))

        log_str = "In the file {}, there are {} records are found ".format(f, len(gps_records))
        print(log_str)
        result.append(log_str)

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    str_re = "{} : ================================================================".format(
        dt_string
    )
    print(str_re)
    result.append(str_re)
    return result


def mcp_with_date(date):
    print("call the function to calculate the mcp with data {}".format(date))
    log_files = [
        join(path, f)
        for f in listdir(path)
        if isfile(join(path, f)) and f.__contains__(date)
    ]
    result = process_gps_records(log_files)
    return result


def mcp_without_date():
    log_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    result = process_gps_records(log_files)
    return result


def mcp_today():
    today = datetime.now().strftime("%Y_%m_%d")
    mcp_with_date(today)


def mcp_yesterday():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y_%m_%d")
    mcp_with_date(yesterday)


if __name__ == "__main__":
    # mcp_today()
    schedule.every().day.at("00:10").do(mcp_today)
    schedule.every().day.at("00:10").do(mcp_yesterday)

    schedule.every().day.at("06:00").do(mcp_today)
    schedule.every().day.at("12:00").do(mcp_today)
    schedule.every().day.at("18:00").do(mcp_today)
    schedule.every().day.at("23:00").do(mcp_today)

    # schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(60)
