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


app = Flask(__name__)
print ('hahaha')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    lists = ["www.ics.uci.edu", "www.ics.uci.edu/faculty.html"]
    return render_template('search.html', urls = lists)

@app.route('/', methods=['GET'])
def index():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)
    # req = request.args.lists()

    # print("Request:" + str(req))
    # #print(json.dumps(req, indent=4))

    # res = {"content": "shabi"}

    # res = json.dumps(res, indent=4)
    # print(res)
    # r = make_response(res)
    # r.headers['Content-Type'] = 'application/json'
    # return r

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    # logging.basicConfig(level=logging.DEBUG,
    #             format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #             datefmt='%a, %d %b %Y %H:%M:%S',
    #             filename='app.log',
    #             filemode='w')
    # logging.debug('This is debug message')
    # logging.info('This is info message')
    # logging.warning('This is warning message')

    print "Starting app on port %d" % port

app.run(debug=False, port=port, host='0.0.0.0')