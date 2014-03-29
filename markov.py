'''
Markov class to generate new text from corpus

Inspired by
http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
'''

import nltk

class Markov(object):
	'''Markov class to generate new text from corpus'''
	def __init__(self, open_file):
		self.open_file = open_file
		self.tokens = self.file_to_tokens()
		self.text = nltk.Text(self.tokens)
	
	def file_to_tokens(self):
		raw = self.open_file.read()
		return nltk.word_tokenize(raw)
	
	def generate_text(self, size=15):
		return self.text.generate(size)

def main():
	fileRepu = open('./data/corpora/republican.txt', 'rb')
	myMarkov = Markov(fileRepu)
	genText = myMarkov.generate_text()
	print genText

if __name__ == '__main__':
	main()