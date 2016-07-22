import urllib
import json
import pandas as pd
from collections import Counter
import datetime
import dateutil.relativedelta
import time
import csv


info=[]
count= {}

url="https://api.meetup.com/2/groups?&sign=true&photo-host=public&category_id=34&country=IN&city=Bangalore&only=name,id,created,topics&key=3c2f404715287713157b6b747e507969"

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
    temp = i['topics']
    # print i['id']
    for j in temp:
        t = j['name']
        t = t.encode('ascii',errors='ignore')
        if t in count:

          if s < 1293840000:                          #2010
            count[t][0] = count[t][0]+1

          if s > 1293840000 and s < 1325376000:       #2010 to 2011
            count[t][1] = count[t][1]+1

          if s > 1325376000 and s < 1356998400:       #2011 to 2012
            count[t][2] = count[t][2]+1

          if s > 1356998400 and s < 1388534400:       #2012 to 2013
            count[t][3] = count[t][3]+1

          if s > 1388534400 and s < 1420070400:       #2013 to 2014
            count[t][4] = count[t][4]+1

          if s > 1420070400 and s < 1451606400:       #2014 to 2015
            count[t][5] = count[t][5]+1

          if s > 1451606400 :                         #2015 to 2016
            count[t][6] = count[t][6]+1


        else:
          count[t] = [0,0,0,0,0,0,0]

          if s < 1293840000:                          #2010
            count[t][0] = count[t][0]+1

          if s > 1293840000 and s < 1325376000:       #2010 to 2011
            count[t][1] = count[t][1]+1

          if s > 1325376000 and s < 1356998400:       #2011 to 2012
            count[t][2] = count[t][2]+1

          if s > 1356998400 and s < 1388534400:       #2012 to 2013
            count[t][3] = count[t][3]+1

          if s > 1388534400 and s < 1420070400:       #2013 to 2014
            count[t][4] = count[t][4]+1

          if s > 1420070400 and s < 1451606400:       #2014 to 2015
            count[t][5] = count[t][5]+1

          if s > 1451606400 :                         #2015 to 2016
            count[t][6] = count[t][6]+1

    


      # s=datetime.datetime.fromtimestamp(s).strftime('%Y')
      # info.append([i['id'],s])
    

  if meta['next'] == '':
    break
  else:
    url = meta['next']

# for i in range(len(info)):
# 	print info[i]
for i in count:
  print i
  print count[i]

with open('folder2/Bangalore.csv', 'w') as myfile:
    wr = csv.writer(myfile, delimiter=',')
    wr.writerow(("Topic","2010","2011","2012","2013","2014","2015","2016"))
    for i in count:
      wr.writerow((i,count[i][0],count[i][1],count[i][2],count[i][3],count[i][4],count[i][5],count[i][6]))
    # wr.writerows(info)


