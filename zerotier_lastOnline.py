import requests
import datetime
import locale

# Set URL and API token variables
network_id = "XXXXXXXXX"
api_token = "YYYYYYYYYYYYYYYYYYYYYYYYYYY"
max_hour_lastOnline = 48

def ITdata (timestamp): 
    dt = datetime.datetime.fromtimestamp(timestamp/1000)
    return dt.strftime('%d %b %Y %H:%M:%S')

def getDiffTime(timestamp1, timestamp2):
    # Convert timestamps to Unix timestamp format
    datetime1 = datetime.datetime.fromtimestamp(int(timestamp1) / 1000)
    datetime2 = datetime.datetime.fromtimestamp(int(timestamp2) / 1000)
    # Calcola la differenza tra i due datetime
    timedelta = datetime2 - datetime1
    # Extracts the hours, minutes and seconds from the difference
    days = timedelta.days
    hour, remainder = divmod(timedelta.seconds, 3600)
    min, sec = divmod(remainder, 60)
    hour += 24*days
    return hour, min, sec

# Performs the GET request to the Zerotier API with the specified API token header
url = f"https://api.zerotier.com/api/v1/network/{network_id}/member"
headers = {"Authorization": f"Bearer {api_token}"}
response = requests.get(url, headers=headers)

# Check if the request was successful and if the response is valid
response.raise_for_status()

# For debug print the JSON obtained from the response
# print(response.json())

data = response.json()
data = sorted(data, key=lambda x: x["lastOnline"], reverse=True)

#Print the node list header
desc = "MyZeroTier Node"
lt = (50-len(desc))//2
print ("\n","-"*lt, desc, "-"*lt)

#print cycle
for member in data:
    clock = member["clock"]
    member_lastOnline = member["lastOnline"]
    member_id = member["id"]
    member_ip = member["config"]["ipAssignments"]
    member_name = member["name"]
    DiffTime = getDiffTime(member_lastOnline, clock)
    hour, min, sec = DiffTime
    if (hour < max_hour_lastOnline):
        print(f"Member ID: {member_id}")
        print(f"Managed IP: {member_ip}")
        print(f"Member Name: {member_name}")
        print(f"lastSeen {hour}:{min}:{sec} hh:mm:ss ago", "|", ITdata(member_lastOnline))
        print("-" * 52)
