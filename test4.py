import urllib
import json
import pandas as pd








resp = urllib.urlopen("https://api.meetup.com/2/events?offset=0&format=json&limited_events=False&group_id=18183575%2C18203773&only=group%2Cname&photo-host=public&page=500&fields=&order=time&status=past&desc=false&sig_id=198475034&sig=bf0328cb9bd67c81b15b2f43296c39814c3308b5")
data2 = json.loads(resp.read())
data2=data2["meta"]
resp.close()

print data2['count']

# name,group_id = [],[]

# for i in data2 :
#  name.append(i['name'])
#  group_id.append(i['group'] ['id'])

# print name
# print group_id