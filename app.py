#!/usr/bin/env python
#encoding=utf-8

"""
短网址
"""

import os
import sys
import StringIO
from flask import Flask, request, redirect, url_for, render_template, abort, send_from_directory, send_file, jsonify, session
import redis
import qrcode

import url

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.urandom(32).encode('hex')
)
#redis
r = redis.StrictRedis(host="localhost", port=6379, db=0)


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
    longUrl = r.get(url)
    if longUrl:
        return redirect("http://" + longUrl, 301)
    else:
        abort(404)


@app.route('/<url>.qr')
def showQRCode(url):
    '''显示短网址对应二维码'''
    if not r.get(url):
        abort(404)
    img = qrcode.make(request.url_root + url)
    buf = StringIO.StringIO()
    img.save(buf, 'png')
    buf.seek(0)
    #img = Image.open(StringIO.StringIO()(img_data))
    return send_file(buf, mimetype='image/png')


def containsAny(seq, aset):
    '''检查seq是否仅包含aset中有的字符'''
    for c in seq:
        if c not in aset:
            return False
    return True


def storeToRedis(shortUrl, longUrl, durationInHours):
    '''存储短网址对应关系到redis'''
    if not r.setnx(shortUrl, longUrl) and r.get(shortUrl) != longUrl:
        return False
    #保存到会话中
    myUrls = session.get('myUrls', dict())
    myUrls[longUrl] = shortUrl
    session['myUrls'] = myUrls
    #更新生存时间
    if durationInHours > 0:
        return r.expire(shortUrl, durationInHours * 3600)
    return True


@app.route('/shortURL', methods=['POST'])
def shortURL():
    longUrl = request.form.get('longUrl', None)
    shortUrl = request.form.get('shortUrl', None)
    duration = int(request.form.get('duration', "-1"))
    if longUrl is None or len(longUrl.strip()) < 3:
        return render_template("index.html", error="请输入长网址！")
    #如果用户有定义短网址则检测短网址是否可用
    if shortUrl:
        if len(shortUrl.strip()) < 3:
            return render_template("index.html", error="自定义短网址长度必须大于等于3！")
        elif not containsAny(shortUrl, url.codeArray):
            return render_template("index.html", error="自定义短网址只可以由数字、大小写字母、下划线(_)和中划线(-)组成！")
        elif not storeToRedis(shortUrl, longUrl, duration):
            return render_template("index.html", error="自定义短网址已存在！")
    else:
        success = False
        for shortUrl in url.shortenURL(longUrl):
            if storeToRedis(shortUrl, longUrl, duration):
                success = True
                break
        if not success:
            return render_template("index.html", error="短网址生成失败TAT...")
    return redirect(url_for("index"))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
    app.run(host='0.0.0.0', debug=True)
