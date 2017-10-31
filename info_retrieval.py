import re
from stop_list import *
import math
import sys
import numpy as np
queries_as_string = open( "cran.qry", 'r').read().replace("\n", "").replace("\r", " ")
queries_as_string2 = open( "cran2.qry", 'r').read().replace("\n", "").replace("\r", " ")
abstracts_as_string2 = open( "cran.all.14002", 'r').read().replace("\n", " ").replace("\r", " ")
#line breaks removed, everything compressed into one string

######### [cleaning methods]
def clean(corpus_as_array): #private method 
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

def get_queries(corpus_as_string):
	corpus_as_array = re.split(".I \d{3} .W ", corpus_as_string) 
	corpus_as_array = filter(None, corpus_as_array)
	# ['this is one . ', 'this is two . ']
	
	for i in xrange(len(corpus_as_array)):
	 	corpus_as_array[i] = corpus_as_array[i].replace(" . ", " ").replace(",", "").replace("?", "").replace("!", "").replace(")", "").replace("(", "") # replace ' . ' >> ['this is one', 'this is two']
	 	corpus_as_array[i] = filter(None, corpus_as_array[i].split(" ")) # split into words >> [['this', 'is', 'one'], ['this', 'is', 'two'] ]	 	
	
	corpus_as_array = clean(corpus_as_array)
	return corpus_as_array

def get_abstracts(corpus_as_string):
	corpus_as_array = re.split(".I [^W]+\.W", corpus_as_string)
	corpus_as_array = filter(None, corpus_as_array)
	# ['experiment one .', 'experiment two .']

	for i in xrange(len(corpus_as_array)):
	 	corpus_as_array[i] = corpus_as_array[i].replace(" .", " ").replace(" . ", " ").replace(",", "").replace("?", "").replace("!", "").replace(")", "").replace("(", "").replace("\\", "").replace("/", "") #> ['this is one', 'this is two']
	 	corpus_as_array[i] = filter(None, corpus_as_array[i].split(" ")) # split into words >> [['this', 'is', 'one'], ['this', 'is', 'two'] ]	 	
	
	corpus_as_array = clean(corpus_as_array)
	return corpus_as_array

######### [tfidf]

def getTF(word, doc): #private
	termFreq = 0;
	for current_word in doc:
		if(current_word == word):
			termFreq = termFreq + 1
	return termFreq

def countDocsContainingWord(one_word, corpus_as_array): #private
	numDocsContainingWord = 0
	for doc in corpus_as_array:
		if one_word in doc:
			numDocsContainingWord = numDocsContainingWord + 1
	return numDocsContainingWord

def getIDF(word, corpus_as_array): #private
	idf = 0.0
	numDocs = len(corpus_as_array)
	numDocsContainingWord = countDocsContainingWord(word, corpus_as_array)
	if(numDocsContainingWord == 0):
		printf("OOV: %s"%word)
	else:
		idf = math.log(numDocs / numDocsContainingWord)
		#print("=====\nnumDocsContainingWord = %d" % numDocsContainingWord) #DB
		#print("ln(%d/%d)\n=====" % (numDocs, numDocsContainingWord)) #DB
	return idf # common (225/110) = 0.69, rare (225/1) = 5.4

def getTFIDF(word, target_file, corpus): #private
	tf = getTF(word, target_file)
	idf = getIDF(word, corpus)
	tfidf = tf * idf
	return tfidf

def getUniqueWords(doc): #corpus is array of arrays #private
	unique_words = []
	
	for words in doc:
		unique_words.append(words) # one list of words
	unique_words = list(set(unique_words)) # unique words
	# print(unique_words) # DB
	return unique_words

#uniq = getUniqueWords("dog pet store dog dog".split(" "))
#print(uniq)

def createTFIDFMatrix(corpus):
	# creating query keys 1 to 225
	keys = []
	for i in xrange(len(corpus)):
		keys.append(i+1)

	columnsMap = {}
	k = 0
	for doc in corpus:
		unique_words = getUniqueWords(doc)
		# initializing empty vector for every doc
		columnsMap[keys[k]] = [0] * len(unique_words)
		k = k + 1
		print(unique_words)

	# populating hashmap
	for c in xrange(len(corpus)):
		unique_words = getUniqueWords(corpus[c]) # unique words per doc
		for r in xrange(len(unique_words)):
			currentWord = unique_words[r]
			tfidf = getTFIDF(currentWord, corpus[c], corpus)
			columnsMap[c+1][r] = tfidf
	return columnsMap

#def printNice(columnsMap):

queries_corpus2 = get_queries(queries_as_string2)
queries_TFIDF2 = createTFIDFMatrix(queries_corpus2)
print(queries_TFIDF2)

abstract_corpus2 = get_abstracts(abstracts_as_string2)
abstract_TFIDF2 = createTFIDFMatrix(abstract_corpus2)
print(abstract_TFIDF2)

#######
'''
abstract_corpus2 = get_abstracts(abstracts_as_string2)
abstract_TFIDF2 = createTFIDFMatrix(abstract_corpus2)

queries_corpus2 = get_queries(queries_as_string2)
queries_TFIDF2 = createTFIDFMatrix(queries_corpus2)
print(queries_TFIDF)


queries_corpus = get_queries(corpus_as_string2)
target_word = "similarity"
target_query = queries_corpus[0]
target_corpus = queries_corpus

tf = getTF(target_word, target_query)
idf = getIDF(target_word, target_corpus)
tfidf = getTFIDF(target_word, target_query, target_corpus)
createTFIDFMatrix(queries_corpus)

print("TF    = %3d\nIDF   = %3.2f\ntfidf = %3.2f" % (tf, idf, tfidf))
'''
#ifd = getIDF("flight", queries_corpus)
#print("hello " == "hello ")
#numAre = countDocsContainingWord("", queries_corpus)
#print(numAre)

