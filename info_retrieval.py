import re
from stop_list import *
import math
import sys
corpus_as_string = open( "cran.qry", 'r').read().replace("\n", "").replace("\r", " ")
corpus_as_string2 = open( "cran2.qry", 'r').read().replace("\n", "").replace("\r", " ")


def get_queries(corpus_as_string):
	corpus_as_array = re.split(".I \d{3} .W ", corpus_as_string) 
	corpus_as_array = filter(None, corpus_as_array)
	# ['this is one . ', 'this is two . ']
	
	for i in xrange(len(corpus_as_array)):
	 	corpus_as_array[i] = corpus_as_array[i].replace(" . ", " ").replace(",", "").replace("?", "").replace("!", "") # replace ' . ' >> ['this is one', 'this is two']
	 	corpus_as_array[i] = filter(None, corpus_as_array[i].split(" ")) # split into words >> [['this', 'is', 'one'], ['this', 'is', 'two'] ]	 	
	return corpus_as_array

def clean(corpus_as_array):
	i = 0
	for doc in corpus_as_array:
		for i in xrange(len(doc)):
			if re.match(r"(\d)+(.)?((\d)+)?", doc[i]): # remove numbers
				doc[i] = ""
			elif doc[i] in closed_class_stop_words: # remove stopword
				doc[i] = ""

	i = 0
	for i in xrange(len(corpus_as_array)):
		corpus_as_array[i] = filter(None, corpus_as_array[i]) # remove blanks

	return(corpus_as_array)

def countDocsContainingWord(one_word, corpus_as_array):
	numDocsContainingWord = 0
	for doc in corpus_as_array:
		if one_word in doc:
			numDocsContainingWord = numDocsContainingWord + 1
	return numDocsContainingWord

def getIDF(word, corpus_as_array):
	numDocs = len(corpus_as_array)
	numDocsContainingWord = countDocsContainingWord(word, corpus_as_array)
	if(numDocsContainingWord == 0):
		print(word)
		print("OOV")
		idf = 0
	else:
		idf = math.log(numDocs / numDocsContainingWord)
		#print("ln(%d/%d)" % (numDocs, numDocsContainingWord)) //DB
	print idf # common (225/110) = 0.69, rare (225/1) = 5.4

def getTF(target_word, doc):
	termFreq = 0;
	for doc_word in doc:
		if(doc_word == target_word):
			termFreq = termFreq + 1
	return termFreq

queries_corpus = clean(get_queries(corpus_as_string))
tf = getTF("similarity", queries_corpus[1])
print(tf)

#ifd = getIDF("flight", queries_corpus)
#print("hello " == "hello ")
#numAre = countDocsContainingWord("", queries_corpus)
#print(numAre)

