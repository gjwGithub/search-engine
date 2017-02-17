from pymongo import MongoClient
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
import tokenize as tokenize
import nltk
from collections import OrderedDict
import json
from pprint import pprint
import sys

def forwardIndex(filename):
	client = MongoClient()
	db = client.SearchEngine
	posts = db.ForwardIndex.find({'document': filename}, {'_id': False})
	if posts.count() >= 1:
		print 'Already have!'
		ForwardIndex = posts[0]
		pprint(ForwardIndex)
		return
	#result = table.insert_one({"test document": {"hao": 1, "tang": 1}})
	doc = html.document_fromstring(open(filename).read())
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True   
	doc = cleaner.clean_html(doc)
	#print doc.text_content()
	plaintext = "\n".join(etree.XPath("//text()")(doc))
	# tokens = nltk.word_tokenize(plaintext)
	# for token in tokens:
	# 	print token
	ForwardIndex = {"document": filename, "tokens": tokenize.tokenize(plaintext)}
	db.ForwardIndex.insert_one(ForwardIndex)

def middle(fromCollection, toCollection):
	client = MongoClient()
	db = client.SearchEngine
	posts = db[fromCollection].find({}, {'_id': False})
	for post in posts:
		if db[toCollection].find({'document': post['document']}, {'_id': False}).count() >= 1:
			print "Find one middle" + post['document']
			continue
		words = {}
		for i, token in enumerate(post['tokens']):
			if words.has_key(token):
				words[token]['frequency'] += 1
				words[token]['position'].append(i)
			else:
				words[token] = {}
				words[token]['frequency'] = 1
				words[token]['position'] = [i]

		InterIndex = {"document": post['document'], "words": words}
		InterIndex['total'] = len(post['tokens'])	
		db[toCollection].insert_one(InterIndex)
		pprint(InterIndex)

def main(argv):
	middle("ForwardIndex", "Middle")
	if len(argv) >= 1:
		filename = argv[0]
	else:
		print "No file as input. Please add text file path to the command."
		return
	#forwardIndex(filename)


if __name__ == "__main__":
	main(sys.argv[1:])
	#forwardIndex(filename);