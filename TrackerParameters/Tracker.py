import requests 

# data = '{"trackerCommandType": "TrackerCommandToChangeParam", "deviceEUIList": "20635F00C8000016", "TRACKING_UL_PERIOD": "120"}'
# data = '{
#   "trackerCommandType": "TrackerCommandToChangeMode",
#   "deviceEUIList": "20635F00C8000016",
#   "newMode":"PERMANENT"
# }'

data="""{
  "trackerCommandType": "TrackerCommandToChangeMode",
  "deviceEUIList": "20635F00C8000016",
  "newMode":"OFF"
}"""

url = 'https://dx-api.thingpark.com/location-trackercommand/latest/api/trackerCommands'

header={}
header.update({'Content-Type':'application/json'})
header.update({'Accept':'application/json'})
header.update({'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjMzNjAxIl0sImV4cCI6MTU3NDIwNTQwOCwianRpIjoiMzRlNDc2MTYtMzFiOC00N2Q4LWE1ZmYtM2I3ODBjZWM4NmQ0IiwiY2xpZW50X2lkIjoiaW90LWFwaS9hY2liaWxzQG5tc3UuZWR1In0.kR1amDsEkKqL9b_PzhsSiK5f4k2fzQbUCEs4V359EayQT_DTnAR4J65lzBxnckAfuQopO9K-77PZrhtQ8LrxOA#&#33;/TrackerCommand/post_trackerCommands'})

req = requests.post(url, data=data, headers=header)
print(req.content)