import sys
from sys import platform
import os

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = 'C:\\range_project_new'

sys.path.append(os.path.join(home_folder, 'statistics'))

from record_count import record_count_with_date, record_count

result = record_count()

str_result: str = ""
for s in result:
    str_result += s + "\n"
str_result += "The GPS records refresh finished !!!!!.\n"

print(str_result)