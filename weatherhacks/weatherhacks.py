#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Weatherhacs module. """

import urllib
import json
from datetime import datetime
import emoji
import xmltodict
import primary_area

# 日毎お天気クラス
class WeatherDate(object):
    # クラス変数
    sun = ("晴", ":sun:")
    cloud = ("曇", ":cloud:")
    rain = ("雨", ":umbrella:")
    snow = ("雪", ":snowman:")

    # コンストラクタ
    def __init__(self, date, telop, temp_max, temp_min, image_url):
        self.date = date
        self.telop = telop
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.image_url = image_url

    # 順番に結果を並べる
    def __orderTelopType(self, telop, text, indexPrev, telop_type):
        index = telop.find(telop_type[0])
        if index != -1:
            if indexPrev > index:
                text = telop_type[1] + text
            else:
                text += telop_type[1]

        return (text, index)

    # 予報を絵文字に変換
    def __telopIcon(self, telop):
        text = ""
        indexPrev = -1

        # 含まれていれば絵文字として出力
        for telop_type in [WeatherDate.sun, WeatherDate.cloud, WeatherDate.rain, WeatherDate.snow]:
            (text, index) = self.__orderTelopType(telop, text, indexPrev, telop_type)
            if indexPrev < index:
                indexPrev = index

        return text

    # 詳細
    def yohou(self, icon):
        text = "【{0}】\n".format(self.date)
        text +=  "{0}".format(self.telop)

        if icon:
            text += self.__telopIcon(self.telop)

        temp = ""
        if self.temp_max:
            temp = "最高 {0}度".format(self.temp_max)

        if self.temp_min:
            if temp:
                temp += "\n"
            temp += "最低 {0}度".format(self.temp_min)

        if temp:
            text += "\n" + temp

        if icon:
            return emoji.emojize(unicode(text, "utf_8"), use_aliases=True)
        else:
            return text

# 全体お天気クラス
class Weather(object):
    # クラス変数
    today = "今日"
    tommorow = "明日"
    dayAfterTomorrow = "明後日"

    # コンストラクタ
    def __init__(self, city, public_time, description, weather_date_list):
        self.city = city
        self.public_time = public_time
        self.description = description
        self.weather_date_list = weather_date_list

    # ダイジェスト
    def digest(self):
        text = "【{0}{1}市】\n{2} 現在の天気予報です。\n".format(self.city.pref_name, self.city.name, self.public_time)

        text += "【説明】\n"
        description_text = ""
        description_list = self.description.splitlines()
        for description in description_list:
            if not description:
                continue
            if description_text:
                description_text += "\n"
            description_text += description

        text += description_text
        return text

    # 対象日の予報
    def __weatherDate(self, date):
        for thisDate in self.weather_date_list:
            if thisDate.date == date:
                return thisDate
        return None

    # 予報
    def yohou(self, date, icon=False):
        weather_date = self.__weatherDate(date)
        if weather_date is not None:
            return weather_date.yohou(icon)
        else:
            return ""

    # 天気画像URL
    def imageUrl(self, date):
        weather_date = self.__weatherDate(date)
        if weather_date is not None:
            return weather_date.image_url
        else:
            return ""


# お天気情報JSONを取得
def getWeatherHacksJson(city):

    # Weather Hacks API URL
    url = "http://weather.livedoor.com/forecast/webservice/json/v1"

    try:
        # GET通信
        html = urllib.urlopen("{0}?city={1}".format(url, city.city_id))
        html_json = json.loads(html.read().decode('utf-8'))
        return html_json

    except Exception as e:
        raise e
        return {}

# お天気情報を変換
def serializeWeather(city, weather_json):
    # 詳細
    public_time = ""
    description = ""
    if weather_json["description"]:
        # 2018-03-12T10:31:00+0900
        time = weather_json["description"]["publicTime"].encode("utf-8")
        date = datetime.strptime(time.replace("+0900", ""), '%Y-%m-%dT%H:%M:%S')
        public_time = date.strftime("%Y/%m/%d %H:%M")

        description = weather_json["description"]["text"].encode("utf-8")

    # 日毎の予報
    weather_date_list = []
    for forecast in weather_json["forecasts"]:
        # どの日
        date = ""
        if forecast["dateLabel"]:
            date = forecast["dateLabel"].encode("utf-8")

        # 予報
        telop = ""
        if forecast["telop"]:
            telop = forecast["telop"].encode("utf-8")

        # 最高気温
        temp_max = ""
        if forecast["temperature"]["max"]:
            temp_max = forecast["temperature"]["max"]["celsius"]

        # 最低気温
        temp_min = ""
        if forecast["temperature"]["min"]:
            temp_min = forecast["temperature"]["min"]["celsius"]

        # 予報画像URL
        image_url = ""
        if forecast["image"]["url"]:
            image_url = forecast["image"]["url"]

        # 日毎お天気
        weather_date = WeatherDate(date, telop, temp_max, temp_min, image_url)
        weather_date_list.append(weather_date)

    # お天気
    weather = Weather(city, public_time, description, weather_date_list)
    return weather

# お天気情報を取得
def getWeatherHacks(city_name):

    # 市情報を検索
    city = primary_area.searchCity(city_name)

    if city:
        # 最新に更新
        weather_json = getWeatherHacksJson(city)

        # お天気情報を取得
        weather = serializeWeather(city, weather_json)

        return weather

    return None

# main
if __name__ == "__main__":

    ############

    try:
        starttime = datetime.now()

        # 最新を取得
        weather = getWeatherHacks("大阪")

        print weather.digest()
        for date in [Weather.today, Weather.tommorow, Weather.dayAfterTomorrow]:
            print weather.yohou(date)
            print weather.yohou(date, icon=True)
            print weather.imageUrl(date)

        endtime = datetime.now()

        # 結果
        print "success! get time: {0}sec".format((endtime-starttime).seconds)

    except Exception as e:
        print "exception! get: {0}".format(e)
