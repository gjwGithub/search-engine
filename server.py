import urllib
import json
import os
import requests
import re
import sys
import math

import random
from flask import Flask, render_template, redirect
from flask import request
from flask import make_response
import score


app = Flask(__name__)

numOfPages = 10 

def PageLink(query, count):
    results = list()
    for i in range(0, count / numOfPages + 1):
        start = i * numOfPages
        results.append({"number": str(i + 1), "url": "http://localhost:5000/search?query={}&start={}".format(query, start)})
    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    start = request.args.get('start')
    if start == None:
        start = 0
    else:
        start = int(start)
    end = start + numOfPages
    results, time, count = score.getDocuments(query, start, end)
    pageLinks = PageLink(query, count)
    return render_template('search.html', results = results, time=time, length = count, pageLinks = pageLinks)

@app.route('/', methods=['GET'])
def index():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=False, port=port, host='0.0.0.0')