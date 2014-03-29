'''
Markov class to generate new text from corpus

Inspired by
http://agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/
http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
'''

import nltk

class Markov(object):
	'''Markov class to generate new text from corpus'''
	def __init__(self, open_file, n):
		self.open_file = open_file
		self.tokens = self.file_to_tokens()
		self.n = n
		self.model = nltk.NgramModel(self.n, self.tokens)

	def file_to_tokens(self):
		raw = self.open_file.read()
		return nltk.word_tokenize(raw)
	
	def generate_text(self, size=20):
		# return self.text.generate(size)
		starting_words = self.model.generate(100)[-2:]
		starting_words = ['we', 'believe']
		content = self.model.generate(size, starting_words)
		return ' '.join(content)

	def ensure_ending(self, text):
		'''Ensure nicer sentence ending'''
		if "!" in text:
			return text[:text.index(".")+1]
		elif "?" in text:
			return text[:text.index(".")+1]
		elif "." in text:
			return text[:text.index(".")+1]
		else:
			return self.ensure_ending(self.generate_text())

def main():
	fileRepu = open('./data/corpora/republican.txt', 'rb')
	print "now generating RepubliCrat tweet..."
	myMarkov = Markov(fileRepu,3)
	genText = myMarkov.generate_text()
	finalText = myMarkov.ensure_ending(genText)

	print "\n*****\n"
	print finalText
	print "\n*****\n"

if __name__ == '__main__':
	main()