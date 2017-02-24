import json
from lxml import html,etree
import urlparse
import sys
import numpy

def InvertBookkeeping():
    dirname = "WEBPAGES_RAW/"
    f = open(dirname + "bookkeeping.json")
    bookkeeping = json.loads(f.read())
    inverted = dict()
    for key in bookkeeping:
        newkey = "http://" + bookkeeping[key]
        # if newkey[-1] != "/":
        #     newkey += "/"
        # if inverted.has_key(newkey):
        #     print key + newkey
        inverted[newkey] = key
    f.close()
    f = open("InvertedBookKeeping.json", "w")
    f.write(json.dumps(inverted, indent=4))
    f.close()

def OutLinks(filename, url):
    results = list()
    try:
        f = open(filename)
        content = f.read()
        page = etree.HTML(content.lower())
        hrefs = page.xpath(u"//a")    
        for href in hrefs:
            rawHref = href.get("href")
            absHref = urlparse.urljoin(url, rawHref)
            if absHref[-1] != "/":
                absHref += "/"
            results.append(absHref)
        del content
        del page
        del hrefs
    except:
        print filename + ": " + str(sys.exc_info()[1]) + "\n"
    finally:
        f.close()
    return results

def ID(filename):
    s = filename.split("/")
    return int(s[0]) * 500 + int(s[1])

def GenerateGraph():
    dirname = "WEBPAGES_RAW/"
    f = open(dirname + "bookkeeping.json")
    bookkeeping = json.loads(f.read())
    f.close()
    f = open("InvertedBookKeeping.json")
    invertedBookkeeping = json.loads(f.read())
    f.close()
    length = len(bookkeeping)
    #f = open("graph.txt", "w")
    graph = numpy.zeros((length, length))
    for i, key in enumerate(bookkeeping):
        # outlinks = OutLinks(dirname + key, "http://" + bookkeeping[key])
        # row = [0.0] * length
        # for link in outlinks:
        #     if invertedBookkeeping.has_key(link):
        #         row[ID(invertedBookkeeping[link])] = 1.0 
        # graph.append(row)
        # del row
        # del outlinks

        outlinks = OutLinks(dirname + key, "http://" + bookkeeping[key])
        for link in outlinks:
            if link[-1] == "/":
                if invertedBookkeeping.has_key(link):
                    graph[i][ID(invertedBookkeeping[link])] = 1.0
                if invertedBookkeeping.has_key(link[:-1]):
                    graph[i][ID(invertedBookkeeping[link[:-1]])] = 1.0
            else:

                if invertedBookkeeping.has_key(link):
                    graph[i][ID(invertedBookkeeping[link])] = 1.0
                if invertedBookkeeping.has_key(link + "/"):
                    graph[i][ID(invertedBookkeeping[link + "/"])] = 1.0
        del outlinks

        # for i, r in enumerate(row):
        #     if i < len(row) - 1:
        #         f.write(str(r) + " ")
        #     else:
        #         f.write(str(r) + "\n")
    #f.close()
    return graph

# if __name__ == "__main__":
#     dirname = "WEBPAGES_RAW/"
#     f = open(dirname + "bookkeeping.json")
#     bookkeeping = json.loads(f.read())
#     key = "0/2"
#     print bookkeeping[key]
#     print OutLinks(dirname + key, "http://" + bookkeeping[key])

#     absHref = urlparse.urljoin("www.ics.uci.edu/alumni/stayconnected/stayconnected/hall_of_fame/hall_of_fame/stayconnected/stayconnected/hall_of_fame/hall_of_fame/hall_of_fame/stayconnected/hall_of_fame/hall_of_fame/hall_of_fame/stayconnected/index.php", '/faculty/area/')
#     print absHref

#     GenerateGraph()