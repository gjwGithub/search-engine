from pymongo import MongoClient
from lxml import html
from lxml import etree
from lxml.html.clean import Cleaner
import tokenize as tokenize
from collections import OrderedDict
import json
import time
import math
from pprint import pprint
import sys

client = MongoClient()
db = client.SearchEngine    
    
def calculateLength(fromCollection, toCollection):
    length = {}
    #start_time = time.time()
    for posting in db[fromCollection].find({}, {'_id': False}):
        for word, posts in posting.iteritems():
            for post in posts:
                if length.has_key(post['document']):
                    length[post['document']] += post['tf-idf']**2
                else:
                    length[post['document']] = post['tf-idf']**2
    db[toCollection].insert_one(length)
    #print("--- %s seconds ---" % (time.time() - start_time))

def main(argv):
    if len(argv) >= 1:
        pprint(calculateLength(argv[0]))
    else:
		print "No toCollection as input."
		return

if __name__ == "__main__":
	main(sys.argv[1:])