from decentlab import query

df = query(domain='nmsu.decentlab.com',
           api_key='eyJrIjoiWHJwTEZTWHNxd1RZWnZzWDJnYWdkMHVjM3RCM0VyTTUiLCJuIjoiYWNpYmlsc0BhZC5ubXN1LmVkdSIsImlkIjoxfQ==',
           time_filter='',
           #include_network_sensors=True,
           device='//',
           sensor='//',
           timezone='America/Denver')

df.to_csv("download.csv")

print(df.head(5))
print("==================================================================")
print(df.shape)
print("==================================================================")


list_dates = list()
for t in list(df.index):
    if t.date() not in list_dates:
        list_dates.append(t.date())

for t in list_dates:
    print (t)
