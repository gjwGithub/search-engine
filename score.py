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
import config
import urlparse
import re

K = 100
client = MongoClient()
db = client.SearchEngine

dirname = "WEBPAGES_RAW/"
f = open(dirname + "bookkeeping.json").read()
bookkeeping = json.loads(f)

f = open("DocumentItems.json").read()
documentItems = json.loads(f)

f = open("PageRank.json").read()
pageRanks = json.loads(f)

tables = ["InvertedIndex", "BoldInvertedIndex", "H3InvertedIndex", "H2InvertedIndex", "H1InvertedIndex", "TitleInvertedIndex"]

weights = {
    "InvertedIndex": 1.0,
    "BoldInvertedIndex": 2.0,
    "H3InvertedIndex": 2.0,
    "H2InvertedIndex": 3.0,
    "H1InvertedIndex": 4.0,
    "TitleInvertedIndex": 5.0
}

vectorLengths = {
    "InvertedIndex": "VectorLength",
    "BoldInvertedIndex": "BoldVectorLength",
    "H3InvertedIndex": "H3VectorLength",
    "H2InvertedIndex": "H2VectorLength",
    "H1InvertedIndex": "H1VectorLength",
    "TitleInvertedIndex": "TitleVectorLength"
}

N = db.ForwardIndex.find({}).count()

def getScore(query):
    start_time = time.time()
    words = tokenize.computeWordFrequencies(tokenize.tokenize(query))
    allOriginalScores = {}

    tfidfs = getOriginalScore("InvertedIndex", allOriginalScores, words) #allOriginalScores is soft copied
    getOriginalScore("BoldInvertedIndex", allOriginalScores, words)
    getOriginalScore("TitleInvertedIndex", allOriginalScores, words)
    getOriginalScore("H1InvertedIndex", allOriginalScores, words)
    getOriginalScore("H2InvertedIndex", allOriginalScores, words)
    getOriginalScore("H3InvertedIndex", allOriginalScores, words)

    #modifyScore(allOriginalScores, score)
    score = {}
    for key in allOriginalScores:
        score[key] = allOriginalScores[key]["InvertedIndex"]

    score = rescale(score)
    allOriginalScores = rescaleAllOriginalScores(allOriginalScores)
    tfidfs = rescale(tfidfs)
    return score, allOriginalScores, tfidfs

def getOriginalScore(table, allOriginalScores, words):
    queryLength = 0
    tfidfs = {}
    for term in words:
        posts = db[table].find({term:{"$exists":True}}, {'_id': False})
        score = {}
        if posts.count() >= 1:
            postList = posts[0][term]
            df = len(postList)
            tfidf = (1 + math.log10(words[term])) * math.log10(float(N) / (df + 1))
            queryLength += tfidf ** 2
            for post in postList:
                tfidfs[post['document']] = post['tf-idf']
                if allOriginalScores.has_key(post['document']):
                    if allOriginalScores[post['document']].has_key(table):
                        allOriginalScores[post['document']][table] += tfidf * post['tf-idf']
                    else:
                        allOriginalScores[post['document']][table] = tfidf * post['tf-idf']
                else:
                    temp = {}
                    temp[table] = tfidf * post['tf-idf']
                    allOriginalScores[post['document']] = temp

    VectorLength = db[vectorLengths[table]].find({}, {'_id': False})[0]
    for key in allOriginalScores:
        if allOriginalScores[key].has_key(table):
            allOriginalScores[key][table] = allOriginalScores[key][table] / math.sqrt(VectorLength[key]) / math.sqrt(queryLength)

    return tfidfs

def modifyScore(allOriginalScores, score):
    for document in allOriginalScores:
        weightCount = 0
        for table in weights:
            if allOriginalScores[document].has_key(table):
                weight = weights[table]
                weightCount += weight
                if score.has_key(document):
                    score[document] += weight * allOriginalScores[document][table]
                else:
                    score[document] = weight * allOriginalScores[document][table]
        score[document] /= weightCount

def rescale(score):
    min = sys.maxint
    max = 0
    for key in score:
        if score[key] > max:
            max = score[key]
        if score[key] < min:
            min = score[key]
    delta = max - min
    for key in score:
        if delta != 0:
            score[key] = (score[key] - min) / delta
        else:
            score[key] = 0    
    return score

def rescaleAllOriginalScores(allOriginalScores):
    for table in tables:
        min = sys.maxint
        max = 0
        for key in allOriginalScores:
            if allOriginalScores[key].has_key(table) and allOriginalScores[key][table] > max:
                max = allOriginalScores[key][table]
            if allOriginalScores[key].has_key(table) and allOriginalScores[key][table] < min:
                min = allOriginalScores[key][table]
        delta = max - min
        for key in allOriginalScores:
            if allOriginalScores[key].has_key(table):
                if delta != 0:
                    allOriginalScores[key][table] = (allOriginalScores[key][table] - min) / delta
                else:
                    allOriginalScores[key][table] = 0
    return allOriginalScores

def getPageRank(score):
    pageRank = {}
    for key in score:
        pageRank[key] = float(pageRanks[key])
    pageRank = rescale(pageRank)
    return pageRank

def combineScoreAndPageRank(score, pageRank, allOriginalScores = None, tfidfs = None):
    result = {}
    if not config.useMachineLearning:
        for key in score:
            result[key] = 0.2 * score[key] + 0.8 * pageRank[key]
    else:
        for key in score:
            if allOriginalScores[key].has_key("BoldInvertedIndex"):
                bold = allOriginalScores[key]["BoldInvertedIndex"]
            else:
                bold = 0
            if allOriginalScores[key].has_key("H3InvertedIndex"):
                h3 = allOriginalScores[key]["H3InvertedIndex"]
            else:
                h3 = 0
            if allOriginalScores[key].has_key("H2InvertedIndex"):
                h2 = allOriginalScores[key]["H2InvertedIndex"]
            else:
                h2 = 0
            if allOriginalScores[key].has_key("H1InvertedIndex"):
                h1 = allOriginalScores[key]["H1InvertedIndex"]
            else:
                h1 = 0
            if allOriginalScores[key].has_key("TitleInvertedIndex"):
                title = allOriginalScores[key]["TitleInvertedIndex"]
            else:
                title = 0
            result[key] = config.weights[0] * score[key] + config.weights[1] * pageRank[key] + config.weights[2] * tfidfs[key] \
                + config.weights[3] * bold + config.weights[4] * title + config.weights[5] * h1 + config.weights[6] * h2 + config.weights[7] * h3
    return result

def getDocuments(query, start, end):
    start_time = time.time()
    score, allOriginalScores, tfidfs = getScore(query)
    print "getScore" + str(time.time() - start_time)
    pageRank = getPageRank(score)
    print "getPageRank" + str(time.time() - start_time)
    if not config.useMachineLearning:
        finalRank = combineScoreAndPageRank(score, pageRank)
    else:
        finalRank = combineScoreAndPageRank(score, pageRank, allOriginalScores, tfidfs)
    print "combineScoreAndPageRank" + str(time.time() - start_time)

    sorted_key_list = sorted(finalRank, key=finalRank.get, reverse = True)

    domainPath = set()
    sorted_key_list2 = list()
    for key in sorted_key_list:
        url = bookkeeping[key[13:]]
        pos = url.find("?")
        path = url[:pos]
        if path not in domainPath and is_valid("http://" + url):
            domainPath.add(path)  
            sorted_key_list2.append(key)
    sorted_key_list = sorted_key_list2
    
    print "sorted_key_list" + str(time.time() - start_time)
    results = []
    for i, document in enumerate(sorted_key_list):
        if i >= end: break
        if i >= start and i < end:
            results.append(getDocumentItem(document))
    return results, time.time() - start_time, len(sorted_key_list)

def getDocumentItem(document):   
    url = bookkeeping[document[13:]]
    if not documentItems.has_key(document):
        title = bookkeeping[document[13:]].split('/')[-1]
        abstract = "Not available"
    else:
        documentItem = documentItems[document]
        title = documentItem['title']
        if title == "":
            title = bookkeeping[document[13:]].split('/')[-1]
        abstract = documentItem['abstract']
    return {"url": url, "title": title, "abstract": abstract}

def is_valid(url):
    if re.match(r"^.*/datasets/datasets/.*$", url): #duplicate path in url #https://support.archive-it.org/hc/en-us/articles/208332963-Modify-your-crawl-scope-with-a-Regular-Expression
        return False
    return True

def main(argv):
    if len(argv) >= 1:
        score, allOriginalScore, tfidfs = getScore(argv[0])
        import copy
        score2 = copy.deepcopy(score)
        score2 = rescale(score2)
        pageRank = getPageRank(score)
        pageRank2 = copy.deepcopy(pageRank)
        pageRank2 = rescale(pageRank2)
        finalRank = combineScoreAndPageRank(score2, pageRank2)
        sorted_key_list = sorted(finalRank, key=finalRank.get, reverse = True)

        domainPath = set()
        sorted_key_list2 = list()
        for item in sorted_key_list:
            url = bookkeeping[item[13:]]
            pos = url.find("?")
            path = url[:pos]
            if path not in domainPath:
                domainPath.add(path)  
                sorted_key_list2.append(item)
        sorted_key_list = sorted_key_list2

        f = open("acm.txt", "w")
        for key in sorted_key_list:
            if allOriginalScore[key].has_key("BoldInvertedIndex"):
                bold = allOriginalScore[key]["BoldInvertedIndex"]
            else:
                bold = 0
            if allOriginalScore[key].has_key("H3InvertedIndex"):
                h3 = allOriginalScore[key]["H3InvertedIndex"]
            else:
                h3 = 0
            if allOriginalScore[key].has_key("H2InvertedIndex"):
                h2 = allOriginalScore[key]["H2InvertedIndex"]
            else:
                h2 = 0
            if allOriginalScore[key].has_key("H1InvertedIndex"):
                h1 = allOriginalScore[key]["H1InvertedIndex"]
            else:
                h1 = 0
            if allOriginalScore[key].has_key("TitleInvertedIndex"):
                title = allOriginalScore[key]["TitleInvertedIndex"]
            else:
                title = 0
            f.write(str(score[key]) + " " + str(pageRank[key]) + " " + str(tfidfs[key]) + " " + str(bold) + " " + str(title) + " " + str(h1) + " " + str(h2) + " " + str(h3) + " " + bookkeeping[key[13:]] + "\n")
        f.close()
    else:
		print "No query as input."
		return

if __name__ == "__main__":
	main(sys.argv[1:])
