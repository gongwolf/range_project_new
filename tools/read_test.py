import tools.gps_tools

f = "data.json"
gps_records = tools.gps_tools.read_Json(f)

print(len(gps_records))

