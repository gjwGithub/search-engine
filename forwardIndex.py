from pymongo import MongoClient
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
import tokenize as tokenize
from collections import OrderedDict
import json
from pprint import pprint
import sys

client = MongoClient()
db = client.SearchEngine

def ProcessForwardIndex(table, plaintext, filename):
	posts = table.find({'document': filename}, {'_id': False})
	if posts.count() >= 1:
		print 'Already have!'
		ForwardIndex = posts[0]
		pprint(ForwardIndex)
		return

	ForwardIndex = {"document": filename, "tokens": tokenize.tokenize(plaintext)}
	table.insert_one(ForwardIndex)

def forwardIndex(filename):
	global db
	ForwardIndex = {"document": filename, "tokens": tokenize.tokenize(plaintext)}
	db.ForwardIndex.insert_one(ForwardIndex)

	ProcessForwardIndex(db.ForwardIndex, Content(filename), filename)
	ProcessForwardIndex(db.BoldForwardIndex, Bold(filename), filename)
	ProcessForwardIndex(db.TitleForwardIndex, Title(filename), filename)
	h1 = H1(filename)
	h2 = H2(filename)
	h3 = H3(filename)
	header = h1 + h2 + h3
	ProcessForwardIndex(db.H1ForwardIndex, h1, filename)
	ProcessForwardIndex(db.H2ForwardIndex, h2, filename)
	ProcessForwardIndex(db.H3ForwardIndex, h3, filename)
	ProcessForwardIndex(db.HeaderForwardIndex, header, filename)

def Content(filename):
	doc = html.document_fromstring(open(filename).read())
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True   
	doc = cleaner.clean_html(doc)
	plaintext = "\n".join(etree.XPath("//text()")(doc))
	return plaintext

def Bold(filename):
	content = open(filename).read()
	page = etree.HTML(content.decode('utf-8'))
	strongs = page.xpath(u"//strong")
	boldStr = str()
	for s in strongs:
		if s.text != None:
			boldStr += s.text + "\n"
		else:
			a = list(s.iter("a"))
			for s2 in a:
				boldStr += s2.text + "\n"
	return boldStr

def Title(filename):
	content = open(filename).read()
	page = etree.HTML(content.decode('utf-8'))
	titles = page.xpath(u"//title")
	TitleStr = str()
	for s in titles:
		TitleStr += s.text + "\n"
	return TitleStr

def H1(filename):
	content = open(filename).read()
	page = etree.HTML(content.decode('utf-8'))
	H1s = page.xpath("//h1")
	H1Str = str()
	for h in H1s:
		if h.text != None:
			H1Str += h.text + "\n"
		else:
			span = list(h.iter("span"))
			for s in span:
				H1Str += s.text + "\n"
	return H1Str

def H2(filename):
	content = open(filename).read()
	page = etree.HTML(content.decode('utf-8'))
	H2s = page.xpath("//h2")
	H2Str = str()
	for h in H2s:
		if h.text != None:
			H2Str += h.text + "\n"
		else:
			span = list(h.iter("span"))
			for s in span:
				H2Str += s.text + "\n"
	return H2Str

def H3(filename):
	content = open(filename).read()
	page = etree.HTML(content.decode('utf-8'))
	H3s = page.xpath("//h3")
	H3Str = str()
	for h in H3s:
		if h.text != None:
			H3Str += h.text + "\n"
		else:
			span = list(h.iter("span"))
			for s in span:
				H3Str += s.text + "\n"
	return H3Str

def middle(fromCollection, toCollection):
	global db
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