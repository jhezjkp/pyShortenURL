#!/usr/bin/env python
#encoding=utf-8

"""
短网址
"""

import os
import random
from flask import Flask, request, redirect, url_for, render_template, abort, send_from_directory, jsonify

import url

app = Flask(__name__)
urlPool = dict()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template("index.html")


@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html")


@app.route('/<url>')
def gotoURL(url):
    #print request.headers
    #print request.remote_addr
    longUrl = urlPool.get(url)
    if longUrl:
        return redirect("http://" + longUrl, 301)
    else:
        abort(404)


@app.route('/shortURL', methods=['POST'])
def shortURL():
    longUrl = request.form['url']
    shortUrl = url.shortenURL(longUrl)[random.randint(0, 3)]
    print shortUrl
    urlPool[shortUrl] = longUrl
    #return jsonify(shortUrl)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
