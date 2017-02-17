from pymongo import MongoClient
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
import tokenize as tokenize
import nltk
from collections import OrderedDict
import json

#string = open("faculty.html").read()
doc = html.document_fromstring(open("faculty.html").read())
cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True   
doc = cleaner.clean_html(doc)
#print doc.text_content()
plaintext = "\n".join(etree.XPath("//text()")(doc))
# tokens = nltk.word_tokenize(plaintext)
# for token in tokens:
# 	print token
ForwardIndex = {"document": "faculty.html", "tokens": tokenize.tokenize(plaintext)}
#print json.dumps(ForwardIndex, indent=4)

words = {}
for i, token in enumerate(ForwardIndex['tokens']):
	if words.has_key(token):
		words[token]['frequency'] += 1
		words[token]['position'].append(i)
	else:
		words[token] = {}
		words[token]['frequency'] = 1
		words[token]['position'] = [i]

InterIndex = {"document": "faculty.html", "words": words}
InterIndex['total'] = len(ForwardIndex['tokens'])
#InterIndex = json.dumps(InterIndex, indent = 4)
print InterIndex

#print InterIndex['document']
InvertedIndex = {}
for word, value in InterIndex['words'].iteritems():
	#print float(value['frequency']) / InterIndex['total']
	if InterIndex.has_key(word):
		posting = {"document": "faculty.html", "tf": float(value['frequency']) / InterIndex['total']}
		InvertedIndex[word].append(posting)
	else:
		InvertedIndex[word] = []
		posting = {"document": "faculty.html", "tf": float(value['frequency']) / InterIndex['total']}
		InvertedIndex[word].append(posting)
print json.dumps(InvertedIndex, indent=4)

# d = tokenize.computeWordFrequencies(tokenize.tokenize(plaintext))
# od = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
# print od


for elt in doc.iter('href'):
	text=elt.text_content()
	print text

# client = MongoClient()
# db = client.SearchEngine
# table = db.ForwardIndex
# #result = table.insert_one({"test document": {"hao": 1, "tang": 1}})
# for document in table.find():
# 	print document