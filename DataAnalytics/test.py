import csv

somedict = dict(raymond='red', rachel='blue', matthew='green')
with open('mycsvfile.csv','wb') as f:
    w = csv.writer(f)
    w.writerows(somedict.items())