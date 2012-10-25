#!/usr/bin/env python
#encoding=utf-8

"""
短网址
"""

import os
from flask import Flask, request, redirect, render_template, abort, send_from_directory

app = Flask(__name__)
urlPool = {'163': 'http://www.163.com'}


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
def shortURL(url):
    #print request.headers
    #print request.remote_addr
    longUrl = urlPool.get(url)
    if longUrl:
        return redirect(longUrl, 301)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
