#!/usr/bin/env python
# -*_ coding:utf-8 -*-
 
import sys
import urllib2
import json

files = []
if len(sys.argv) > 1:
	for file in sys.argv[1:]:
		files.append(str(file))
else:
	print "Usage: xwords.py file1 file2 file3 ..."
 
text = ""
for file in files:
	f = open(file,"rU")
	for line in f:
		text += line
 
words = text.lower().split()
wordcount = {}

for word in words:
	if word.isalpha() and len(word)>2:
		if word in wordcount:
			wordcount[word] += 1
		else:
			wordcount[word] = 1
		
frequency =  sorted(wordcount,key=wordcount.get,reverse=True)
 
shanbay_api = 'https://api.shanbay.com/bdc/search/?word='

for word in frequency:
    res = urllib2.urlopen(shanbay_api+word)
    js = json.load(res)
    if js['status_code']==0 :
        pronun = js['data']['pronunciation'].encode('utf-8')
        defin = js['data']['definition'].encode('utf-8').replace('\n','\t')
        print wordcount[word],word,'/'+pronun+'/',defin
