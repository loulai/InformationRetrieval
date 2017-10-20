import re
from stop_list import *
queries = open( "cran.qry", 'r')

def trim(string):
	trimmed_words = (re.sub(r"([\d]|[.\,!?()\[\]\-\%@#$^*;\\\/\|<>\"\'_+=:{\}.])+", "", string)).split(" ")
	stop_words = closed_class_stop_words
	for stop_word in stop_words:
		while stop_word in trimmed_words: 
			trimmed_words.remove(stop_word)
	return(trimmed_words)

def get_tf(array):
	# takes an array of terms without punctuation and stopwords
	terms = list(set(array))#unique
	term_frequency = dict.fromkeys(terms, 0) #dict with default value 0
	for word in array:
		term_frequency[word] = term_frequency[word] + 1

	return term_frequency

def print_dict(dictionary):
	for key, value in dictionary.items():
		print(key, value)

#print(trim("Hello! [I'm!] Mc-cool! (Muahaha).... and over being diamons"))
test = ("cat dog cat cat lemon").split(" ")
print_dict(get_tf(test))


