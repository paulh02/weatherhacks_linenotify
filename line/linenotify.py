#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Posted LINE Notify module. """

import os
import urllib
import urllib2
import json
from datetime import datetime

# LINE Notify に通知する
def postLineNotify(token, message="", image_url=""):

    # LINE Notify API URL
    url = "https://notify-api.line.me/api/notify"

    # リクエストパラメータ
    headers = { "Authorization": "Bearer {0}".format(token) }
    payload = {}

    # メッセージ追加
    if message:
        payload["message"] = message

    # 画像追加
    if image_url:
        payload["imageThumbnail"] = image_url
        payload["imageFullsize"] = image_url

    try:
        payload = urllib.urlencode(payload).encode("utf-8")
        req = urllib2.Request(url, payload, headers=headers)
        urllib2.urlopen(req)

    except Exception as e:
        raise e

# main
if __name__ == "__main__":

    # LINE Notify お天気 トークン
    line_token = os.environ["LINE_NOTIFY_OTENKI_TOKEN"]

    ############

    try:
        starttime = datetime.now()

        # 通知
        postLineNotify(line_token, message="テストですよ。")

        # 通知
        postLineNotify(line_token, message="テストなのですよ。", image_url="http://en.freejpg.com.ar/asset/900/65/65ab/F100011060.jpg")

        endtime = datetime.now()

        print "success! post time: {0}sec".format((endtime-starttime).seconds)

    except Exception as e:
        print "exception! get: {0}".format(e)
