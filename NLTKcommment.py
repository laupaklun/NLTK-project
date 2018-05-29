import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def make_dictionary(dict, incrementers_Sample, decrementers_Sample, small_degree_Sample, opposite_Sample):
	small_degree = []  # score*1.5 , factor=1.5
	incrementers = []  # score*2 , factor=2
	decrementers = []  # score/2 ,factor = 0.5
	opposite = []  # score*-1.0, factor = -1

	lemmatize = WordNetLemmatizer()
	seed_dict = {}
	allowed_word_types = ["J", "R", "V"]

	for all_words in dict:
		synonyms = []
		antonyms = []
		score = dict[all_words]

		for syn in wordnet.synsets(all_words):
			for l in syn.lemmas():
				synonyms.append(l.name())
				if l.antonyms():
					antonyms.append(l.antonyms()[0].name())
		synonyms.append(all_words)
		for word in synonyms:
			seed_dict[word] = score
		for word in antonyms:
			seed_dict[word] = -score

	for inc in incrementers_Sample:
		for word in wordnet.synsets(inc):
			for l in word.lemmas():
				string = l.name
				incrementers.append(string)

	for dec in decrementers_Sample:
		for word in wordnet.synsets(dec):
			for l in word.lemmas():
				string = l.name
				decrementers.append(string)

	for sd in small_degree_Sample:
		for word in wordnet.synsets(sd):
			for l in word.lemmas():
				string = l.name
				small_degree.append(string)

	for opp in opposite_Sample:
		for word in wordnet.synsets(opp):
			for l in word.lemmas():
				string = l.name
				opposite.append(string)

	print('Dictionary Completed!')
	return small_degree, incrementers, decrementers, opposite

def main():
	dict = {'glad':1.0,'know':1.0,'unnecessary':-1.0,'important':1.0,'advantage':1.0,'great':1.0,'gorgeous':1.0,\
			'thank':1.0, 'deny':-1.0,'fun':1.0, 'nice':1.0,'negative':-1.0,'positive':1.0,'awesome':1.0,'effective'\
				:1.0,'good':1.0, 'bad':-1.0,'like':1.0 ,'brilliant':1.0,'smart':1.0,'appreciate':1.0, 'disagree':\
				-1.0, 'agree':1.0}
	incrementers_Sample={'strong','definitely','honestly','very','really','too','extremely','undobutly'}
	decrementers_Sample={'little','barely'}
	small_degree_Sample={'actually','pretty','fairly','quite','rather','so','slightly'}
	opposite_Sample={'should','dont','not',"n't", 'n\'t','oppositely'}
	small_degree, incrementers, decrementers, opposite = make_dictionary(\
		dict,incrementers_Sample,decrementers_Sample,small_degree_Sample,opposite_Sample)

	i = 0
	factors = []
	factors.append(1)
	totalscore = 0
	dictcount = 0

	def setdata():
		del factors[:]
		factors.append(1)
		mark=0

	def calscore(word):
		global mark
		global factors
		global totalscore
		global dictcount

		if word in incrementers:
			factors.append(2)
			return
		elif word in decrementers:
			factors.append(0.5)
			return
		elif word in small_degree:
			factors.append(1.5)
			return
		elif word in opposite:
			factors.append(-1)
			return
		elif word in seed_dict:
			global mark
			print(word)
			mark = seed_dict.get(word)
			for obj in factors:
				mark= mark*obj
				totalscore=totalscore+mark
				dictcount += 1
				setdata()
				return

	with open('input.txt', mode='r') as file_in:
		test_txt = file_in.read()
	sent_tokens = sent_tokenize(test_txt)
	words = word_tokenize(test_txt)
	stop_words = set(stopwords.words("english"))
	filtered_sentence = []
	for w in words:
		if w not in stop_words:
			filtered_sentence.append(w)

	ps = PorterStemmer()

	for words in filtered_sentence:
		words = ps.stem(words)
	word_tokens = []
	file_in.close()

	for sent in sent_tokens:
		if sent[:2]=='~~':  # first two item
			i+=1
			if (dictcount) > 0:
				print ('Blog post '+str(i)+' score: '+str.format('{0:.2f}', totalscore*10/dictcount)+"/10")
				totalscore=0
				dictcount=0

			else:
				print('Blog post '+str(i)+' score: '+str.format('{0:.2f}', totalscore*10)+"/10")
				totalscore=0
				dictcount=0

		word_token = word_tokenize(sent)
		for word in word_token:
			calscore(word)
			word_tokens.append(word_token)

main()