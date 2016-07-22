import urllib
import json
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from scipy import stats


geolocator = Nominatim() #create object
places = ["bangalore"]

urls = [] 
radius = 50.0 
data_format = "json" 
topic = "python"
for place in places:
 print place
 location = geolocator.geocode(place)
 url = "https://api.meetup.com/2/groups?offset=0&format=" + data_format + "&lon=" + str(location.longitude) + "&topic=" + topic + "&photo-host=public&page=500&radius=" + str(radius)+"&fields=&lat=" + str(location.latitude) + "&only=name,members,rating&order=id&desc=false&key=6340751e1a2943497b781a744355e60"
rating,name,members = [],[],[]
print(url)
response = urllib.urlopen(url)
data = json.loads(response.read())
data=data["results"]

for i in data :
 rating.append(i['rating'])
 name.append(i['name'])
 members.append(i['members'])

print name
members_zscore = stats.zscore(members)
rating_zscore = stats.zscore(rating)
# members_zscore.append(stats.zscore(members))
print members_zscore
print rating_zscore

for index in range(len(name)):
   print 'Total Score of %s : %2f' % (name[index] , 10*stats.norm.cdf(0.5 * members_zscore[index] + 0.5 * rating_zscore[index]))




