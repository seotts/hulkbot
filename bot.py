#http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

#!/usr/bin/env python

# -*- coding: utf-8 -*-

import tweepy, time, sys
import feedparser
import random

#enter the corresponding information from your Twitter application:
CONSUMER_KEY = 'oi8UIxO0NCecqQm5MH8u8bv4R'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'ZAadGMreBinURy11dbCKz9JmqGjSSLB0gOPmaJ4RgTc4oH528v'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '3004140602-pb2FuDNlbwjVHpvl0gtOhqgnV7IdqLRCoimJTjb'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'eWBmHJhBSTF3ZJ3sVaF0iSovjO1GLAuGvBrezfVCf6B3I'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


def findAndReplaceYou(text, notWords):

	text = text.upper()
	textWords = text.split()
	newText = [];
	count = 0; 
	for i in range(0, len(textWords)):
		
		t = textWords[i]
		if(t in notWords):
			return []
		elif(t == "YOU" or t == "YOUR" or t == "YOU'RE"):
			count = count+1
			newText.append("HULK")
		elif(t == "YOU'LL"):
			newText.append("HULK WILL")
			count = count+1
		elif(t == "DON'T" or t == "CAN'T"):
			newText.append("NO")
		elif(not(t == "THE" or t == "A" or t == "AN" or t == "IS" or t == "ARE")):
			newText.append(t)
			i = i - 1
		

	if(count < 1):
		return []
	
	return " ".join(newText)		

def notYetPosted(statusText):
	lastTweet = api.home_timeline(count = 1)
	lastText = lastTweet[0].text.replace("!","")
	if(lastText == statusText):
		return False
	return True

#makes a tweet out of a buzzfeed title with "you" in it
def makeATweet(feed):
	found = False 
	i = 0
	edited = "";
	while(not found and i < len(feed['entries'])):
		nextTitle = feed['entries'][i]['title'] 
		edited = findAndReplaceYou(nextTitle, ["I", "I'M", "ME"])
		if(len(edited) > 3):
			found = True
		else:
			i = i+1
	unique = notYetPosted(edited)
	if(unique):
		withExclamation = edited +"!"*random.randint(0,5)
		api.update_status(status=withExclamation)
	else:
		print "already posted"


#create rss feed
buzzfeed = feedparser.parse('http://www.buzzfeed.com/index.xml')
makeATweet(buzzfeed)
#time.sleep(12*60*60)#Tweet every  12 hours
