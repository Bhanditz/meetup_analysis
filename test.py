import urllib
import json
import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
geolocator = Nominatim() #create object
places = ["bangalore"]

urls = [] 
radius = 50.0 
data_format = "json" 
topic = "dstandup"
for place in places:
 print place
 # location = geolocator.geocode(place)
 urls.append("https://api.meetup.com/2/groups?&sign=true&photo-host=public&topic=" + topic + "&radius=50.0&fields=group_photo,next_event,primary_topic,sponsors&country=IN&city="+ place + "&key=3c2f404715287713157b6b747e507969")
city,country,rating,name,members,photo = [],[],[],[],[],[]
for url in urls:
 print url
 response = urllib.urlopen(url)
 data = json.loads(response.read())
 data=data["results"]

print data
for i in data :
 city.append(i['city'])
 country.append(i['country'])
 rating.append(i['rating'])
 name.append(i['name'])
 members.append(i['members'])
 photo.append(i['group_photo']['thumb_link'])


print "Total Group: " 
print len(city)
print rating
print name
print members
