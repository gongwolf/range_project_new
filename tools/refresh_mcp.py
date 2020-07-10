import sys
from sys import platform
import os

if platform == "linux":
    home_folder = "/home/gqxwolf/mydata/range_project_new"
elif platform == "win32":
    home_folder = 'C:\\range_project_new'

sys.path.append(os.path.join(home_folder, 'statistics', 'MCP'))
from MCPCalculation import mcp_without_date, mcp_with_date

result = mcp_without_date()

str_result: str = ""
for s in result:
    str_result += s + "\n"
str_result += "The GPS MCP refresh finished !!!!!.\n"

web_result: str = ""
for s in result:
    web_result += s + "\n"
web_result += "The GPS MCP refresh finished !!!!!.\n"

print(web_result)