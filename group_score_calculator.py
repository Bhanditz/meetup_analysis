import urllib
import time
import json
from collections import Counter

x = raw_input('Enter country name: ')
country = str(x).upper()
print "Entered Country Name :  "+country
y = raw_input('Enter city name: ')
city = str(y)
print "Entered City Name :  "+city
z = raw_input('Enter topic name: ')
t = str(z)
topic = t.replace(' ','-')
print "Entered Topic Name :  "+topic

urls = []
urls.append("https://api.meetup.com/2/groups?&sign=true&photo-host=public&topic=" + topic + "&radius=50.0&fields=next_event,primary_topic,sponsors&country=" + country[:2] + "&city="+ city + "&only=name,id,created,rating,link,sponsors,members,next_event,primary_topic&key=3c2f404715287713157b6b747e507969")

grp_ids,rating,name,members,link,created,next_event_name,next_event_rsvp,primary_topic,sponsors = {},{},{},{},{},{},{},{},{},{}

for url in urls:
  print url
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  meta=data["meta"]
  data=data["results"]
  response.close()

c=0
for i in data :
  grp_ids[c]=i['id']
  print grp_ids[c]
  rating[c]=i['rating']
  print rating[c]
  name[c]=i['name']
  print name[c]
  members[c]=i['members']
  print members[c]
  created[c]=i['created']
  print created[c]
  link[c]=i['link']
  print link[c]
  try:
    primary_topic[c] = i['primary_topic']['name']
  except KeyError:
    primary_topic[c] = " "
  print primary_topic[c]
  sponsors.setdefault(c, [])
  try:
    for j in i['sponsors'] :
      sponsors[c].append(str(j['name'].encode('utf-8')))
  except KeyError:
    sponsors[c] = " "
  print sponsors[c]
  try:
    next_event_name[c]=i['next_event']['name']
    next_event_rsvp[c]=i['next_event']['yes_rsvp_count']
  except KeyError:
    next_event_name[c] = " "
    next_event_rsvp[c] = " "
  print next_event_name[c]
  print next_event_rsvp[c]
  c+=1
  print "\n"

total_grp = meta['total_count']
print "Total Group: " 
print total_grp


leaders={}
c=0
while(c<len(grp_ids)):
  urls=[]
  urls.append("https://api.meetup.com/2/profiles?&sign=true&photo-host=public&role=leads&group_id="+str(grp_ids[c])+"&only=member_id&key=3c2f404715287713157b6b747e507969")
  for url in urls:
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    meta=data["meta"]
    response.close()
  leaders[c]=meta['total_count']
  c+=1

print leaders

events={}
url2 = []
c=0
while(c<len(grp_ids)):
  url2=[]
  url2.append("https://api.meetup.com/2/events?&sign=true&photo-host=public&group_id="+str(grp_ids[c])+"&status=past&only=id&key=3c2f404715287713157b6b747e507969")
  for url in url2:
    resp = urllib.urlopen(url)
    data2 = json.loads(resp.read())
    data2=data2["results"]
    resp.close()
  events.setdefault(c, [])
  for i in data2 :
    try:
      events[c].append(str(i['id']))
    except KeyError:
      events[c] = []
  c+=1

print events

active_members={}
for i in events:
  actv=[]
  c=0
  url3=[]
  url3.append("https://api.meetup.com/2/rsvps?&sign=true&photo-host=public&rsvp=yes&only=member&event_id=")
  l=len(events[i])
  while(c<l):
    url3[0]+=str(events[i][c])
    url3[0]+=","
    c+=1
  url3[0]+="&key=3c2f404715287713157b6b747e507969"
  for url in url3:
    response3 = urllib.urlopen(url)
    data3 = json.loads(response3.read())
    try:
      data3=data3["results"]
    except :
      data3=[]
      response3.close()
  for j in data3:
    actv.append(j['member']['member_id'])
  counts = Counter(actv)
  temp = Counter(el for el in counts.elements() if counts[el] >= (len(events[i])/10))
  active_members[i] = len(temp)
  
print active_members
freq_events={}
c=0
current_epoch_time=time.time()
while(c<len(created)):
  temp=created[c]-current_epoch_time
  if len(events[c]) >= 1:
    freq_events[c]=temp/len(events[c])
  else:
    freq_events[c]=temp
  c+=1
print freq_events #if less then better

