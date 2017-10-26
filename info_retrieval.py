import re
from stop_list import *
queries = open( "cran.qry", 'r').read().replace("\n", "").replace("\r", " ")

def get_query_strings(string):
	query_strings = re.split(".I \d{3} .W ", string)
	return query_strings

