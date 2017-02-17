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

def main(argv):
	if len(argv) >= 1:
		filename = argv[0]
	else:
		print "No file as input. Please add text file path to the command."
		return
	forwardIndex(filename)

if __name__ == "__main__":
	main(sys.argv[1:])
	#forwardIndex(filename);