import os
import urllib
import simplejson as json
from twython import Twython
import pprint
import HTMLParser
import re

import keywords

#twitter credentials
API_KEY = 'BoP0mE4gtGZlh1me29lug'
API_SECRET = 'xteLnU2uu3KEKxZx8hc1wfPic0gs5JvosmRP9VBA6c'
ACCESS_TOKEN = '2417467056-2aZr2bQSGaDcRnbqR7QAHC95TXXSPbyQr2jONYa'
ACCESS_TOKEN_SECRET = 'LBKmR3OXxVFiLEM9zeiYNe0tKwUyiFdfmz27ts36AuhHW'

KEYWORDS = [kw.replace("\n", "") for kw in open('./keywords.txt').readlines()]
GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
HTTPLEFTOVER_PAT = re.compile('https?\S*')

def filter_for_keywords(twTexts, keywords=KEYWORDS):
	return [twText for twText in twTexts if any(kw.lower() in twText.lower() for kw in keywords)]

def stripURLs(text):
	text = text.replace("http : /", "http:/")
	text = text.replace("https : /", "https:/")
	urls = [ "".join(mgroups) for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ]
	for url in urls:
		text = text.replace(url, "")
	httpLeftovers = ["".join(mgroups) for mgroups in HTTPLEFTOVER_PAT.findall(text) ]
	# print "hlo's: "
	# print httpLeftovers
	for hlo in httpLeftovers:
		text = text.replace(hlo, "")
	return text

def main():
	twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	# Get Politicians' Twitter Handles
	apiKey = 'AIzaSyD-mnJ5Gff-xJDpEU78Pc5iXLbMHmK4FPA'
	url = 'https://www.googleapis.com/freebase/v1/search?'

	handles = {'republican':[], 'democratic':[]}
	for party in handles.keys():
		parameters = { 
			'filter': '(all type:politician member_of:' + party + ')',
			'limit': 220,
			'indent': True,
			'spell': 'always',
			'key': apiKey,
			'output' : '(/internet/social_network_user/twitter_id)'
		  };

		parameters = urllib.urlencode(parameters)
		jsonObject = urllib.urlopen(url + parameters).read()
		content = json.loads(jsonObject)
		result = content['result']

		for person in result:
			twitterInfo = person['output']['/internet/social_network_user/twitter_id']
			if twitterInfo != {}:
				handle = twitterInfo['/internet/social_network_user/twitter_id'][0]
				handles[party].append(handle)

	wFileBase = "./data/corpora/tweets-"
	for party in handles.keys():
		# open file for reading and appending
		with open(wFileBase+party+'.txt', 'ab+') as wFile:
			for partyHandle in handles[party]:
				print "now getting TL for "+partyHandle
				try:
					userTL = twitter.get_user_timeline(screen_name=partyHandle)
				except Exception, e:
					continue # skip handles raise error because suspended etc
				twTexts = [tweet['text'] for tweet in userTL]
				relevantTwTexts = filter_for_keywords(twTexts)
				for twText in relevantTwTexts:
					unescapedTwText = HTMLParser.HTMLParser().unescape(twText).encode('utf-8')
					strippedTwText = stripURLs(unescapedTwText)
					finalTwText = strippedTwText
					wFile.seek(0, os.SEEK_SET) # point stream to start of file
					currentText = wFile.read()
					if not finalTwText in currentText:
						wFile.write(finalTwText+"\n")

if __name__ == '__main__':
	main()
				

