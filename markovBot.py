# coding: utf-8
'''
Markov class to generate new text from corpus

Inspired by
http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
'''

import nltk
import re

class MarkovBot(object):
	'''Markov class to generate new text from corpus'''
	def __init__(self, rawText, n):
		# self.open_file = open_file
		self.tokens = self.file_to_tokens(rawText)
		self.n = n
		self.model = nltk.NgramModel(self.n, self.tokens)

	def file_to_tokens(self, rawText):
		# raw = self.open_file.read()
		return nltk.word_tokenize(rawText)
	
	def generate_text(self, size=30):
		starting_words = self.model.generate(100)[-2:]
		# starting_words = ['we', 'believe']
		content = self.model.generate(size, starting_words)
		endedContent = self.ensure_ending(content)
		return endedContent

	def ensure_ending(self, tokens):
		'''Ensure text has sentence ending'''
		ending = re.compile("[\.\!\?]+$")
		for i in range(len(tokens)):
			if ending.search(tokens[i]):
				return tokens[:i+1]
		# no ending found, generate new text
		return self.generate_text()


	def ensure_tweet_length(self, text):
		'''Ensure text is within tweet length'''
		if len(text) <= 140:
			return text
		else:
			return self.ensure_tweet_length(' '.join(self.generate_text()))

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

if __name__ == '__main__':
	main()