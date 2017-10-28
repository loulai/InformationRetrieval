import re
from stop_list import *
import math
import sys
import numpy as np
corpus_as_string = open( "cran.qry", 'r').read().replace("\n", "").replace("\r", " ")
corpus_as_string2 = open( "cran2.qry", 'r').read().replace("\n", "").replace("\r", " ")


def get_queries(corpus_as_string):
	corpus_as_array = re.split(".I \d{3} .W ", corpus_as_string) 
	corpus_as_array = filter(None, corpus_as_array)
	# ['this is one . ', 'this is two . ']
	
	for i in xrange(len(corpus_as_array)):
	 	corpus_as_array[i] = corpus_as_array[i].replace(" . ", " ").replace(",", "").replace("?", "").replace("!", "").replace(")", "").replace("(", "") # replace ' . ' >> ['this is one', 'this is two']
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

def getTF(word, doc):
	termFreq = 0;
	for doc_word in doc:
		if(doc_word == word):
			termFreq = termFreq + 1
	return termFreq

def getIDF(word, corpus_as_array):
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

def getTFIDF(word, target_file, corpus):
	tf = getTF(word, target_file)
	idf = getIDF(word, corpus)
	tfidf = tf * idf
	return tfidf

def getUniqueWords(corpus): #corpus is array of arrays
	giant_words = []
	for doc in corpus:
		for words in doc:
			giant_words.append(words) # one giant list of words
	giant_words = list(set(giant_words)) # unique words
	return giant_words

def createTFIDFMatrix(corpus):
	unique_words = getUniqueWords(corpus)
	keys = []
	for i in xrange(len(corpus)):
		keys.append(i+1)
	columnsMap = {}

	for k in xrange(len(corpus)):
   		columnsMap[keys[k]] = corpus[k]
	
	print columnsMap

queries_corpus = clean(get_queries(corpus_as_string))
createTFIDFMatrix(queries_corpus)


'''
public TFIDF addTFIDF() {

	for(int i = 0; i< nCol; i++) {
		for(int k=0; k< nRow; k++) {
			String currentWord = uniqueTerms.get(k);
			double tfidf = getTFIDF(currentWord, mainCorpus[i], mainCorpus);
			
			//update
			columnsMap.get(String.valueOf(i)).set(k,  tfidf);
		}
	}
	return this;
}
'''

queries_corpus = clean(get_queries(corpus_as_string))
target_word = "similarity"
target_query = queries_corpus[0]
target_corpus = queries_corpus

tf = getTF(target_word, target_query)
idf = getIDF(target_word, target_corpus)
tfidf = getTFIDF(target_word, target_query, target_corpus)
print("TF    = %3d\nIDF   = %3.2f\ntfidf = %3.2f" % (tf, idf, tfidf))



#ifd = getIDF("flight", queries_corpus)
#print("hello " == "hello ")
#numAre = countDocsContainingWord("", queries_corpus)
#print(numAre)

