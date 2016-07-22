from flask import Flask, render_template, request, redirect, url_for, abort, session

import urllib
import json
import pandas as pd
from collections import Counter
import datetime
import dateutil.relativedelta
import time
import operator
from scipy import stats
from operator import itemgetter
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	

	country = request.form['Country'].upper()
	print "Entered Country Name :  "+country
	
	city = request.form['City']
	print "Entered City Name :  "+city
	
	t = request.form['Topic']
	topic = t.replace(' ','-')
	print "Entered Topic Name :  "+topic


	# Accesing group details

	print "Fetching group details"

	url1="https://api.meetup.com/2/groups?&sign=true&photo-host=public&topic=" + topic + "&radius=50.0&fields=next_event,primary_topic,sponsors&country=" + country[:2] + "&city="+ city + "&only=name,id,description,urlname,created,rating,link,sponsors,topics,members,next_event,primary_topic&key=3c2f404715287713157b6b747e507969"

	info,temp_info= {}, {}

	print url1
	response = urllib.urlopen(url1)
	data = json.loads(response.read())
	if "results" in data :
	  data=data["results"]
	  response.close()
	else :
	  print 'The json response doesnot contain results object'
	  quit()


	for i in data :
	  info[i['id']] = [i.get('name'),i['id'],i.get('rating',0),i.get('members',0),i.get('created',0),i.get('description','')]
	  temp_info[i['id']]= []

	print 'Total groups found'
	print len(info)

	# print info

	# Accessing past events
	grp_ids_list = []
	grp_name_list = []
	for i in info:
	  grp_ids_list.append(info[i][1])
	  grp_name_list.append(info[i][0])

	grp_ids_list = '%2C'.join(map(str, grp_ids_list))
	# myList1 = ','.join(map(str, grp_name_list))

	print "Fetching event details"
	url2 = "https://api.meetup.com/2/events?offset=0&format=json&limited_events=True&group_id="+grp_ids_list+"&only=group%2Cid%2Ctime&photo-host=public&page=500&fields=&order=time&status=past&desc=true&key=3c2f404715287713157b6b747e507969"

	print url2
	response = urllib.urlopen(url2)
	data = json.loads(response.read())
	if "results" in data :
	  data=data["results"]
	  response.close()
	else :
	  print 'The json response doesnot contain results object2'
	  quit()

	events_list,frequency = [], []

	for i in data :
	  frequency.append(i['group']['id'])

	counts = Counter(frequency)
	# print counts



	for i in info :
	  if i in counts :
	    info[i].append(counts[i])
	    if counts[i] > 5:
	      info[i].append(5)
	    else:
	      info[i].append(counts[i])

	  else :
	    info[i].append(0)
	    info[i].append(0)

	  # print info[i][1]
	  # print info[i][7]
	  # print info[i][8]


	for i in data :
	  if info[i['group']['id']][7] > 0 :
	    events_list.append(i['id'])
	    info[i['group']['id']][7] = info[i['group']['id']][7] -1

	# print events_list
	events_list = '%2C'.join(map(str, events_list))

	# Accessing active members
	print "Fetching members details"
	url3 ="https://api.meetup.com/2/rsvps?offset=0&format=json&event_id="+events_list+"&only=member%2Cgroup&photo-host=public&page=500&fields=&order=event&desc=false&key=3c2f404715287713157b6b747e507969"

	print url3

	while True:
	  print url3
	  response = urllib.urlopen(url3)
	  data = json.loads(response.read())
	  if "results" in data :
	    meta=data["meta"]
	    data=data["results"]
	    response.close()
	  else :
	    print 'The json response doesnot contain results object3'
	    quit()

	  for i in data :
	    temp_info[i['group']['id']].append(i['member']['member_id'])

	  if meta['next'] == '':
	    break
	  else:
	    url3 = meta['next']

	for i in temp_info :
	  counts = Counter(temp_info[i])
	  # counts = Counter(el for el in counts.elements() if counts[el] >= (info[i][7]/3))
	  # print counts
	  # print len(counts)
	  info[i].append(len(counts))

	# calculating frequency of events
	for i in info :
	  # print info[i][4]
	  dt1 = datetime.datetime.fromtimestamp(info[i][4]/1000) # 1973-11-29 22:33:09
	  dt2 = datetime.datetime.fromtimestamp(time.time()) # 1977-06-07 23:44:50
	  rd = dateutil.relativedelta.relativedelta (dt2, dt1)
	  t = ((rd.years*12)+rd.months)
	  if t != 0:
	    info[i].append(info[i][6]/((rd.years*12)+rd.months))
	  else :
	    info[i].append(info[i][6])

	print "Fetching leads details"
	for i in info :
	  url4 = "https://api.meetup.com/2/profiles?&sign=true&photo-host=public&role=leads&group_id="+str(info[i][1])+"&only=member_id&key=3c2f404715287713157b6b747e507969"
	  print url4
	  response = urllib.urlopen(url4)
	  data = json.loads(response.read())
	  if "meta" in data :
	    meta=data["meta"]
	    response.close()
	  else :
	    print 'The json response doesnot contain results object4'
	    quit()
	  info[i].append(meta['total_count'])


	# calulating Z_Score
	name,grp_id,rating,members,act_members,freq,leads =[],[],[],[],[],[],[]
	for i in info :
	  name.append(info[i][0])
	  grp_id.append(info[i][1])
	  rating.append(info[i][2])
	  members.append(info[i][3])
	  act_members.append(info[i][8])
	  freq.append(info[i][9])
	  leads.append(info[i][10])


	members_zscore = stats.zscore(members)
	members_zscore = [0 if x != x else x for x in members_zscore]

	rating_zscore = stats.zscore(rating)
	rating_zscore = [0 if x != x else x for x in rating_zscore]

	act_members_zscore = stats.zscore(act_members)
	act_members_zscore = [0 if x != x else x for x in act_members_zscore]

	freq_zscore = stats.zscore(freq)
	freq_zscore = [0 if x != x else x for x in freq_zscore]

	leads_zscore = stats.zscore(leads)
	leads_zscore = [0 if x != x else x for x in leads_zscore]

	# print members_zscore
	# print rating_zscore
	# print act_members_zscore
	# print freq_zscore
	# print leads_zscore

	score = []

	for index in range(len(name)):
	    h=info[grp_id[index]][5]
	    soup = BeautifulSoup(h)

	    # unescaped = cgi.escape(h)
	    # print unescaped
	    score.append({'id':grp_id[index] , 'name':name[index],'description':soup.get_text(),'score':round(10*stats.norm.cdf(0.2 * members_zscore[index] + 0.2 * rating_zscore[index] + 0.2 * act_members_zscore[index] + 0.2 * freq_zscore[index] + 0.2 * leads_zscore[index]),1)})

	sorted_score=sorted(score, key=itemgetter('score'),reverse=True) 
	print sorted_score
    
	return render_template('message.html', result=sorted_score, 
                                           topic=topic,city=city)


# @app.route('/message')
# def message():
#     # if not 'username' in session:
#     #     return abort(403)
#     return render_template('message.html', result=session['result'], 
#                                            topic=session['topic'],city=session['city'])

if __name__ == '__main__':
    app.run(debug=True)