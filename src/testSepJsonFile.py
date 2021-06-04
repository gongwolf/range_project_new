import json
import os
import sys
from datetime import date
from tqdm import tqdm
from sys import platform


from src.writeToDisk import processRecord, updateTheCSVFile

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = 'C:\\range_project_new'

sys.path.append(os.path.join(home_folder, 'statistics'))
sys.path.append(os.path.join(home_folder, 'statistics', 'MCP'))

from record_count import record_count_with_date, record_count
from MCPCalculation import mcp_without_date, mcp_with_date

with open('/home/gqxwolf/mydata/range_project_new/src/logs/2021_01_15_gps.log') as f:
    data = json.load(f)

# pbar = tqdm(total=len(data))
# for d in data:
#     pbar.update(1)
#     str_today = date.today().__str__().replace("-", "_")
#     updateTheCSVFile(str_today, d)
# pbar.close()

record_count_with_date("2021_01_15")
mcp_with_date("2021_01_14")

