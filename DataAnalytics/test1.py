import urllib
import json
import pandas as pd
from collections import Counter
import datetime
import dateutil.relativedelta
import time
import csv


info=[]

url="https://api.meetup.com/2/groups?&sign=true&photo-host=public&category_id=34&country=IN&city=Pune&only=name,id,created&key=3c2f404715287713157b6b747e507969"

while True:
  # print url
  response = urllib.urlopen(url)
  data = json.loads(response.read())
  if "results" in data :
    meta=data["meta"]
    data=data["results"]
    response.close()
  else :
    print 'The json response doesnot contain results object3'
    quit()

  for i in data :
    s = i['created']/1000
    
    if s > 1388534400:
    	s=datetime.datetime.fromtimestamp(s).strftime('%Y')
    	info.append([i['id'],s])
    

  if meta['next'] == '':
    break
  else:
    url = meta['next']

for i in range(len(info)):
	print info[i]

with open('Pune2.csv', 'w') as myfile:
    wr = csv.writer(myfile, delimiter=',')
    wr.writerow(("GroupID","Year"))
    wr.writerows(info)
