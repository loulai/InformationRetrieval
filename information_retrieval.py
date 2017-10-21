import re
from stop_list import *
queries = open( "cran.qry", 'r').read()
queries.replace("\s ", "")
print(queries)

def get_query_nums(string):
	query_nums = []
	q1 = re.findall(r".I \d{3}", string)
	for q in q1:
		query_nums.append(q.replace(".I ", ""))
	return(query_nums)

def get_query_strings(string):
	query_strings = []
	q1 = re.findall(r"([a-z ]+\n){1,3}[a-z ]+\.", string)
	print(q1)
	for q in q1:
		query_strings.append(q)
	return(query_strings)


#print(get_query_nums(queries))
get_query_strings(queries)

def trim(string):
	trimmed_words = filter(None,(re.sub(r"\n|\r", " ", string)).split(" ")) #replace line breaks with spaces
	#trimmed_words = filter(None, re.sub(r"\.|,|!|\?", "", trimmed_words).split(" "))  #remove some punctuation, filter blank spaces
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

print(trim(open("cran2.qry", 'r').read()))

#test = ("cat dog cat cat lemon").split(" ")
#print_dict(get_tf(test))


