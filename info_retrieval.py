import re
from stop_list import *
corpus_as_string = open( "cran.qry", 'r').read().replace("\n", "").replace("\r", " ")
corpus_as_string2 = open( "cran2.qry", 'r').read().replace("\n", "").replace("\r", " ")


def get_queries(corpus_as_string):
	queries_as_array = re.split(".I \d{3} .W ", corpus_as_string) 
	queries_as_array = filter(None, queries_as_array)
	final_array_of_arrays = [0] * len(queries_as_array)
	# ['this is one . ', 'this is two . ']
	
	for query in queries_as_array:
	 	query = query.replace(" . ", " ") 
	 	# ['this is one', 'this is two']

	for i in xrange(len(final_array_of_arrays)):
		final_array_of_arrays[i] = filter(None, queries_as_array[i].split(" "))
		# [ ['this', 'is', 'one'], ['this', 'is', 'two'] ]
	return final_array_of_arrays

def countDocsContainingWord(one_word, corpus_as_array):
	numDocsContainingWord = 0
	for doc in corpus_as_array:
		if one_word in doc:
			numDocsContainingWord = numDocsContainingWord + 1
	return numDocsContainingWord

queries_corpus = get_queries(corpus_as_string2)
numAre = countDocsContainingWord("", queries_corpus)
print(queries_corpus)
print(numAre)
