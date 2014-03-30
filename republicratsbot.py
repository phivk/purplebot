from markovBot import *
from twython import Twython

API_KEY = 'BoP0mE4gtGZlh1me29lug'
API_SECRET = 'xteLnU2uu3KEKxZx8hc1wfPic0gs5JvosmRP9VBA6c'
ACCESS_TOKEN = '2417467056-2aZr2bQSGaDcRnbqR7QAHC95TXXSPbyQr2jONYa'
ACCESS_TOKEN_SECRET = 'LBKmR3OXxVFiLEM9zeiYNe0tKwUyiFdfmz27ts36AuhHW'

twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def main():
	rawText1 = open('./data/corpora/republican.txt', 'rb').read()
	rawText2 = open('./data/corpora/democrat.txt', 'rb').read()

	# combine texts by summing equal parts
	minLength = min(len(rawText1), len(rawText2))
	combinedText = rawText1[:minLength] + rawText2[:minLength]

	print "now generating RepubliCrat tweet..."
	myMarkov = MarkovBot(combinedText,3)
	genText = myMarkov.generate_text()
	sentence = ' '.join(genText)
	finalText = myMarkov.ensure_tweet_length(sentence)

	print "\n*****\n"
	print finalText
	print "\n*****\n"

	twitter.update_status(status=finalText)

if __name__ == '__main__':
	main()