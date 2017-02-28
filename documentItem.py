from pymongo import MongoClient
import forwardIndex
import time
from pprint import pprint
import json
import sys
from lxml import html
import re

# client = MongoClient()
# db = client.SearchEngine

def ProcessDocumentItem(filename):
    print "Process DocumentItem"
    t = time.time()
    out = open(filename, "w")
    dirname = "WEBPAGES_RAW/"
    f = open(dirname + "bookkeeping.json").read()
    bookkeeping = json.loads(f)
    result = dict()
    for name in bookkeeping:
        filename = dirname + name
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
    out.write(json.dumps(result, indent=4))
    out.close()
    print "Time: " + str(time.time()-t1)

if __name__ == "__main__":
    ProcessDocumentItem()



