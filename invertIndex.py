from pymongo import MongoClient
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
import tokenize as tokenize
import nltk
from collections import OrderedDict
import json
import sys
import math

def invertedIndex(fromCollection, toCollection):
	idfMap, N = calculateDF(fromCollection)
	for word, df in idfMap.iteritems():
		idfMap[word] = math.log10( float(N) / df)
	InvertedIndex = {}
	client = MongoClient()
	db = client.SearchEngine
	posts = db[fromCollection].find({}, {'_id': False})
	if db[toCollection].find({}, {'_id': False}).count() >= 1:
		db[toCollection].delete_many({})
		print "Deleted all documents in " + toCollection
	for post in posts:
		for word, value in post['words'].iteritems():
			if InvertedIndex.has_key(word):
				itf = 1 + math.log10(value['frequency'])
				InvertedIndex[word].append({"document": post['document'], "tf": itf, "td-idf": itf * idfMap[word]})
			else:
				itf = 1 + math.log10(value['frequency'])
				InvertedIndex[word] = [{"document": post['document'], "tf": itf, "td-idf": itf * idfMap[word]}]
	for word, value in InvertedIndex.items():
		db[toCollection].insert_one({word: value})

def calculateDF(fromCollection):
	client = MongoClient()
	db = client.SearchEngine
	dFMap = {}
	posts = db[fromCollection].find({}, {'_id': False})
	for post in posts:
		for word, value in post['words'].iteritems():
			if dFMap.has_key(word):
				dFMap[word] += 1
			else:
				dFMap[word] = 1
	return (dFMap, db[fromCollection].find({}, {'_id': False}).count())

def main(argv):
	invertedIndex("Middle", "InvertedIndex")

	#forwardIndex(filename)
#print (json.dumps(invertedIndex("Middle", "InvertedIndex"), indent=4))
if __name__ == "__main__":
	main(sys.argv[1:])
	#forwardIndex(filename);