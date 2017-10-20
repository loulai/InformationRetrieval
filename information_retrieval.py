import re
from stop_list import *
queries = open( "cran.qry", 'r')

def trim(string):
	trimmed_words = (re.sub(r"([\d]|[.\,!?()\[\]\-\%@#$^*;\\\/\|<>\"\'_+=:{\}.])+", "", string)).split(" ")
	stop_words = closed_class_stop_words
	for stop_word in stop_words:
		while stop_word in trimmed_words: 
			trimmed_words.remove(stop_word)
	print(trimmed_words)
	return(trimmed_words)

#def get_tf(string):

'''
	line = line.strip("\n")		
	p = line.split("\t")
	if len(p) == 1:
		continue
	words.append(p[0])
	tags.append(p[1])
'''


trim("Hello! [I'm!] Mc-cool! (Muahaha).... and over being diamons")