from markovBot import *
from twython import Twython
import re
import time
import random
import simplejson as json

CORPUS_PATH_DEMOCRAT = './data/corpora/tweets-democratic.txt'
CORPUS_PATH_REPUBLICAN = './data/corpora/tweets-republican.txt'

PROB_NO_MINUTES_INTERVAL = 30

def concat_symbols(text):
	# remove excess symbols from beginning & excess spaces
	symbolEndSet = [':',';','.',',','?','??','!', "'s"]
	for s in symbolEndSet:
		if text[:2] == " "+s:
			text = text[2:]
		if text[:2] == s+" ":
			text = text[2:]
		text = text.replace(" "+s, s)	

	text = text.replace("# ", "#")
	# NB leave "@ [handle]" to prevent @mentions that lead to suspension!

	# remove unmatched quotation chars
	matchSymbols = ['\xe2', "''","``",'"']
	for s in matchSymbols:
		if text.count(s) == 1:
			text = text.replace(s, "")

	# custom replacements
	replaceSet = {
		"does n't ": "doesn't ",
		"do n't": "don't",
		"ca n't": "can't",
		" 've ": "'ve ",
		"??s ": "'s ",
		"ai n't": "ain't",
		"were n't": "weren't",
		"  ": " ",
	}
	for chars, replacement in replaceSet.iteritems():
		text = text.replace(chars, replacement)	

	return text

def get_credentials(filePath):
	with open(filePath) as f:
		CREDS = json.load(f)
	return CREDS

def main():
	CREDS = get_credentials('./credentials.json')
	twitter = Twython(CREDS['API_KEY'], CREDS['API_SECRET'], CREDS['ACCESS_TOKEN'], CREDS['ACCESS_TOKEN_SECRET'])
	
	rawText1 = open(CORPUS_PATH_REPUBLICAN, 'rb').read()
	rawText2 = open(CORPUS_PATH_DEMOCRAT, 'rb').read()

	# combine texts by summing equal parts
	minLength = min(len(rawText1), len(rawText2))
	combinedText = rawText1[:minLength] + rawText2[:minLength]

	print "now generating RepubliCrat tweet..."
	myMarkov = MarkovBot(combinedText,3)

	while 1:
		genText = myMarkov.generate_text()
		sentence = ' '.join(genText)
		tweetText = myMarkov.ensure_tweet_length(sentence)
		tagText = concat_symbols(tweetText)

		finalText = tagText
		try:
			if random.random() < (1.0 / PROB_NO_MINUTES_INTERVAL):
				twitter.update_status(status=finalText)
				print "tweet..."
			else:
				print "skip..."
			print "\n*****\n"
			print finalText
			print "\n*****\n"
		except Exception, e:
			print "\n*****\n"
			print "Error on text: "
			print finalText
			print "\n*****\n"
			raise e
			# continue
		time.sleep(60)


if __name__ == '__main__':
	main()