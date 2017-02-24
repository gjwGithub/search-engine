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

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results, time = score.getScore(query)
    length = len(results)
    return render_template('search.html', results = results, time=time, length = length)

@app.route('/', methods=['GET'])
def index():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=False, port=port, host='0.0.0.0')