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

weights = {
    "InvertedIndex": 1.0,
    "BoldInvertedIndex": 2.0,
    "H3InvertedIndex": 2.0,
    "H2InvertedIndex": 3.0,
    "H1InvertedIndex": 4.0,
    "TitleInvertedIndex": 5.0
}
# for key in weights:
#     totalWeight += weights[key]

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
    score = {}
    allOriginalScores = {}
    # queryLength = 0
    # for term in words:
    #     #print ("{%s:{$exists:true}}, {'_id': false}" % (term))
    #     posts = db.InvertedIndex.find({term:{"$exists":True}}, {'_id': False})
    #     # print posts
    #     #pprint(posts.count())
    #     if posts.count() >= 1:
    #         postList = posts[0][term]
    #         N = db.ForwardIndex.find({}).count()
    #         df = len(postList)
    #         tfidf = (1 + math.log10(words[term])) * math.log10(float(N) / (df + 1))
    #         queryLength += tfidf ** 2
    #         for post in postList:
    #             if score.has_key(post['document']):
    #                 score[post['document']] += tfidf * post['tf-idf']
    #             else:
    #                 score[post['document']] = tfidf * post['tf-idf']


    getOriginalScore("InvertedIndex", allOriginalScores, words)
    getOriginalScore("BoldInvertedIndex", allOriginalScores, words)
    getOriginalScore("TitleInvertedIndex", allOriginalScores, words)
    getOriginalScore("H1InvertedIndex", allOriginalScores, words)
    getOriginalScore("H2InvertedIndex", allOriginalScores, words)
    getOriginalScore("H3InvertedIndex", allOriginalScores, words)

    modifyScore(allOriginalScores, score)

    # VectorLength = {}
    # #for post in db.VectorLength.find({}, {'_id': False}):
    # VectorLength = db.VectorLength.find({}, {'_id': False})[0]

    # for key in score:
    #     score[key] = score[key] / math.sqrt(VectorLength[key]) / math.sqrt(queryLength)

    print("--- %s seconds ---" % (time.time() - start_time))
    #print score

    # sorted_key_list = sorted(score, key=score.get, reverse = True)
    # return sorted_key_list
    score = unify(score)
    return score

def getOriginalScore(table, allOriginalScores, words):
    queryLength = 0
    for term in words:
        posts = db[table].find({term:{"$exists":True}}, {'_id': False})
        score = {}
        if posts.count() >= 1:
            postList = posts[0][term]
            df = len(postList)
            tfidf = (1 + math.log10(words[term])) * math.log10(float(N) / (df + 1))
            queryLength += tfidf ** 2
            for post in postList:
                if allOriginalScores.has_key(post['document']):
                    if allOriginalScores[post['document']].has_key(table):
                        allOriginalScores[post['document']][table] += tfidf * post['tf-idf']
                    else:
                        allOriginalScores[post['document']][table] = tfidf * post['tf-idf']
                else:
                    temp = {}
                    temp[table] = tfidf * post['tf-idf']
                    allOriginalScores[post['document']] = temp
                    # allOriginalScores[post['document']][table] = tfidf * post['tf-idf']
    VectorLength = db[vectorLengths[table]].find({}, {'_id': False})[0]
    for key in allOriginalScores:
        if allOriginalScores[key].has_key(table):
            allOriginalScores[key][table] = allOriginalScores[key][table] / math.sqrt(VectorLength[key]) / math.sqrt(queryLength)

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

def unify(score):
    min = sys.maxint
    max = 0
    for key in score:
        if score[key] > max:
            max = score[key]
        if score[key] < min:
            min = score[key]
    delta = max - min
    for key in score:
        score[key] = (score[key] - min) / delta
    return score

def getPageRank(score):
    pageRank = {}
    for key in score:
        pageRank[key] = float(pageRanks[key])
    pageRank = unify(pageRank)
    return pageRank

def combineScoreAndPageRank(score, pageRank):
    result = {}
    for key in score:
        result[key] = 0.2 * score[key] + 0.8 * pageRank[key]
    return result

def getDocuments(query, start, end):
    start_time = time.time()
    score = getScore(query)
    print "getScore" + str(time.time() - start_time)
    pageRank = getPageRank(score)
    print "getPageRank" + str(time.time() - start_time)
    finalRank = combineScoreAndPageRank(score, pageRank)
    print "combineScoreAndPageRank" + str(time.time() - start_time)

    sorted_key_list = sorted(finalRank, key=finalRank.get, reverse = True)

    domainPath = set()
    sorted_key_list2 = list()
    for key in sorted_key_list:
        url = bookkeeping[key[13:]]
        pos = url.find("?")
        path = url[:pos]
        if path not in domainPath:
            domainPath.add(path)  
            sorted_key_list2.append(key)
    sorted_key_list = sorted_key_list2
    
    print "sorted_key_list" + str(time.time() - start_time)
    results = []
    for i, document in enumerate(sorted_key_list):
        if i >= end: break
        #print "Rank " + str(i) + ": " + document + ". Score: " + str(score[document])
        # results.append({"url": bookkeeping[document[13:]], "title": getTitle(document), "abstract": 'Murray Sherk Murray Sherk Univ. of Waterloo, School of Computer Science msherk@dragon.uwaterloo.ca Author, editor, or reviewer of: Self-adjusting $k$-ary search-trees [ D. Eppstein publications ] [ Citation database ] [ Authors ] Fano Experimental Web Server, D. Eppstein , School of Information & Co...'})
        if i >= start and i < end:
            results.append(getDocumentItem(document))
    return results, time.time() - start_time, len(sorted_key_list)

def getDocumentItem(document):
    # post = db.DocumentItem.find({"document": document}, {'_id': False})
    # url = bookkeeping[document[13:]]
    # if post.count() == 0:
    #     title = bookkeeping[document[13:]].split('/')[-1]
    #     abstract = "Not available"
    # else:
    #     title = post[0]['title']
    #     if title == "":
    #         title = bookkeeping[document[13:]].split('/')[-1]
    #     abstract = post[0]['abstract']
    # return {"url": url, "title": title, "abstract": abstract}
    
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


def getTitle(document):
    post = db.TitleForwardIndex.find({"document": document}, {'_id': False})
    if post.count() == 0:
        return bookkeeping[document[13:]].split('/')[-1]
    else:
        title = ""
        for p in post[0]['tokens']:
            p = p.title()
            title += p + " "
        if title == "":
            return bookkeeping[document[13:]].split('/')[-1]
        return title

def main(argv):
    if len(argv) >= 1:
        #pprint(getScore(argv[0]))
        score = getScore(argv[0])
        pageRank = getPageRank(score)
        f = open("feature.txt", "w")
        for key in score:
            f.write(str(score[key]) + " " + str(pageRank[key]) + "\n")
        f.close()
    else:
		print "No query as input."
		return

if __name__ == "__main__":
	main(sys.argv[1:])
