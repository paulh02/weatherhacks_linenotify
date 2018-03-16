#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
from datetime import datetime
from weatherhacks import weatherhacks
from line import linenotify

# main
if __name__ == "__main__":

    # LINE Notify お天気 トークン
    line_token = os.environ["LINE_NOTIFY_OTENKI_TOKEN"]

    try:
        starttime = datetime.now()

        # 最新の天気予報を取得
        weather = weatherhacks.getWeatherHacks("大阪")

        # 天気予報を通知

        # ダイジェストをまず通知
        linenotify.postLineNotify(line_token, message=weather.digest())

        # 今日、明日、明後日を通知
        for date in [weatherhacks.Weather.today, weatherhacks.Weather.tommorow, weatherhacks.Weather.dayAfterTomorrow]:
            yohou = weather.yohou(date, icon=True).encode("utf_8")
            if yohou:
                linenotify.postLineNotify(line_token, message=yohou)

        endtime = datetime.now()

        # 結果
        print "success! weather time: {0}sec".format((endtime-starttime).seconds)

    except Exception as e:
        print "exception! weather: {0}".format(e)
