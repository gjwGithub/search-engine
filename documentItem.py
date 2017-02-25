from pymongo import MongoClient
import forwardIndex
import time
from pprint import pprint
import json
import sys
from lxml import html
import re

client = MongoClient()
db = client.SearchEngine

#posts = db.InvertedIndex.find({term:{"$exists":True}}, {'_id': False})

# posts = db.InvertedIndex.find({}, {'_id': False})
# f = open("inverted.txt", "w")
# f.write("{\n")
# i = 0
# len = 10
# for i, post in enumerate(posts):
#     if i>=10:
#         break
#     for key in post:
#         f.write("'" + key + "': " + str(post[key]))
#     if i == len-1:
#         f.write("\n")
#     else:
#         f.write(",\n")
    
# f.write("}\n")
# f.close()

# f = open("WEBPAGES_RAW/bookkeeping.json").read()
# inverted = json.loads(f)
# start = time.time()
# print inverted['0/154']
# print inverted['6/45']
# print inverted['12/78']
# print inverted['19/85']
# print inverted['26/14']
# print inverted['33/75']
# print inverted['42/19']
# print inverted['59/51']
# print inverted['68/77']
# print inverted['71/71']
# print("--- %s seconds ---" % (time.time() - start_time))

# f = open("inverted.txt").read()
# # for i in range(0,10):
# #     s = f.readline()
# #     print s
# inverted = json.loads(f)
# print inverted['word']

# start = time.time()
# posts = db.InvertedIndex.find({'regularize':{"$exists":True}}, {'_id': False})[0]
# for key in posts:
#     print posts[key]

#print( db.URLIndex.find({'word':{"$exists":True}}, {'_id': False})[0] )


dirname = "WEBPAGES_RAW/"
f = open(dirname + "bookkeeping.json").read()
bookkeeping = json.loads(f)
out = open("DocumentItems.json", "w")
result = dict()

def ProcessDocumentItem(filename):
    fileContent = open(filename).read()
    try:
        if html.fromstring(fileContent).find('.//*') is not None: #html
            title = forwardIndex.Title(fileContent)
            if title == "":
                title = bookkeeping[filename[13:]].split('/')[-1]
            abstract = str()
            content = forwardIndex.Content(fileContent)
            content = re.sub("\s+", ' ', content) #remove extra space
            content = content.lstrip() #remove spaces at the beginning
            content = content.rstrip() #remove spaces at the end
            if len(content) > 300:
                abstract = content[:300] + "..."
            else:
                abstract = content + "..."
        else: #txt
            title = bookkeeping[filename[13:]].split('/')[-1]
            abstract = str()
            if len(fileContent) > 300:
                abstract = fileContent[:300] + "..."
            else:
                abstract = fileContent
        url = bookkeeping[filename[13:]]
        abstract = abstract.encode('utf-8')
        #insert = {"document": filename, "title": title, "url": url, "abstract": abstract}
        #db.DocumentItem.insert_one(insert)
        result[filename] = {"title": title, "url": url, "abstract": abstract}
    except:
		print filename + ": " + str(sys.exc_info()[1]) + "\n"

if __name__ == "__main__":
    t1 = time.time()
    for name in bookkeeping:
        ProcessDocumentItem(dirname + name)
    out.write(json.dumps(result, indent=4))
    out.close()
    print "Time: " + str(time.time()-t1)

    #ProcessDocumentItem("WEBPAGES_RAW/19/476")



