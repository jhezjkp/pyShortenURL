#!/usr/bin/env python
#encoding=utf-8

"""
短网址
"""

import os
import sys
import random
from flask import Flask, request, redirect, url_for, render_template, abort, send_from_directory, jsonify, session

import url

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.urandom(32).encode('hex')
)
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


def containsAny(seq, aset):
    '''检查seq是否仅包含aset中有的字符'''
    for c in seq:
        if c not in aset:
            return False
    return True

@app.route('/shortURL', methods=['POST'])
def shortURL():
    longUrl = request.form.get('longUrl', None)
    shortUrl = request.form.get('shortUrl', None)
    duration = request.form.get('duration', "0")
    if longUrl is None or len(longUrl.strip()) < 3:
        return render_template("index.html", error="请输入长网址！")
    #如果用户有定义短网址则检测短网址是否可用
    if shortUrl:
        if len(shortUrl.strip()) < 3:
            return render_template("index.html", error="自定义短网址长度必须大于等于3！")
        elif not containsAny(shortUrl, url.codeArray):
            return render_template("index.html", error="自定义短网址只可以由数字、大小写字母、下划线(_)和中划线(-)组成！")
    shortUrl = url.shortenURL(longUrl)[random.randint(0, 3)]
    print shortUrl
    urlPool[shortUrl] = longUrl
    myUrls = session.get('myUrls', dict())
    myUrls[longUrl] = shortUrl
    session['myUrls'] = myUrls
    #return jsonify(shortUrl)
    return redirect(url_for("index"))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    app.run(host='0.0.0.0', debug=True)
