import random
import json
import pickle
import io

start_tok = "*"
end_line_tok = "."


def tokenize(file):
	words = []
	with open(file) as data_file:
		lines = json.load(data_file)
		for line in lines[:]:
			words.extend(line.lower().split()[:-1])
			words.append('.')
	return words

def build_model(words, ngrams=3):

	word_dict = {}

	curr_ngram = [start_tok] * ngrams

	for word in words:
		curr_ngram = curr_ngram[1:] + [word]
		curr_dict = word_dict

		for i in range(ngrams):
			if i < ngrams-1:
				if not curr_dict.has_key(curr_ngram[i]):
					curr_dict[curr_ngram[i]] = {}
				curr_dict = curr_dict[curr_ngram[i]]

			else:
				if not curr_dict.has_key(curr_ngram[i]):
					curr_dict[curr_ngram[i]] = 1
				else:
					curr_dict[curr_ngram[i]] = curr_dict[curr_ngram[i]] + 1

		if curr_ngram[i] == end_line_tok:
			curr_ngram = [start_tok] * ngrams

	return word_dict


def get_word(word_dict, curr_ngram):

	curr_dict = word_dict
	for word in curr_ngram:
		curr_dict = curr_dict[word]
	
	values = 0


	for value in curr_dict.itervalues():
		values = values + value

	rand_val = random.uniform(0, values)

	curr_sum = 0.0
	for key, freq in curr_dict.iteritems():	
		curr_sum += freq
		if rand_val < curr_sum:
			return key
	return key



def generate_sentence(word_dict, ngrams=3, min_length=6, max_length=16):

	sentence = []
	while len(sentence) > max_length or len(sentence) < min_length:
		#reset sentence if it is too long or too short
		sentence=[]
		curr_ngram = [start_tok] * (ngrams-1)
		sentence_end = False
		while not sentence_end:
			word = get_word(word_dict, curr_ngram)
			sentence.append(word)
			if word == end_line_tok:
				#cut off end line token
				sentence = sentence[:-1]
				sentence_end = True
			curr_ngram = curr_ngram[1:] + [word]
	return ' '.join(sentence)


#words = tokenize('lines.json')
#model = build_model(words)
pkl_file = open('model3.pkl', 'rb')
#pickle.dump(model, pkl_file)
print "opened file"
model = pickle.load(pkl_file)
print "loaded model"
print '\a'
with io.open('generated_lines.txt', 'w', encoding='utf8') as file:
	for i in range(0, 10000):
		file.write(generate_sentence(model))
		file.write(u'\n')
		if i % 200 == 0:
			print i
print '\a'


