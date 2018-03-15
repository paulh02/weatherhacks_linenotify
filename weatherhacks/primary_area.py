#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Weatherhacs primary_area module. """

import urllib2
import xmltodict
from datetime import datetime

# 市情報クラス
class City(object):
    # コンストラクタ
    def __init__(self, pref_name, name, city_id):
        self.pref_name = pref_name
        self.name = name
        self.city_id = city_id

# 県情報クラス
class Pref(object):
    # コンストラクタ
    def __init__(self, name, city_list):
        self.name = name
        self.city_list = city_list

# 県情報を取得
def getPrefList():

    # primary_areaのxmlファイルURL
    url = "http://weather.livedoor.com/forecast/rss/primary_area.xml"

    try:
        # ファイル情報取得
        primary_area = urllib2.urlopen(url)

        # 辞書に変換
        primary_area_dict = xmltodict.parse(primary_area)

        # 県情報だけ抜き出し
        pref_list = primary_area_dict["rss"]["channel"]["ldWeather:source"]["pref"]
        if pref_list:
            return pref_list
        else:
            return []

    except Exception as e:
        raise e
        return []

# 市情報を変換
def searializeCity(pref_name, city_dict):
    # 県名
    pref_name_trans = pref_name
    if pref_name in ["道北", "道東", "道南", "道央", "道南"]:
        # 北海道はいっぱいある
        pref_name_trans = "北海道"

    # 名前
    name = ""
    if city_dict["@title"]:
        name = city_dict["@title"].encode("utf-8")

    # ID
    city_id = ""
    if city_dict["@id"]:
        city_id = city_dict["@id"].encode("utf-8")

    # 市
    city = City(pref_name_trans, name, city_id)
    return city

# 県情報を変換
def serializePref(pref_dict):
    # 名前
    pref_name = ""
    if pref_dict["@title"]:
        pref_name = pref_dict["@title"].encode("utf-8")

    # 市リスト
    city_list = []
    if not isinstance(pref_dict["city"], list):
        # 1件しかないとリストじゃない
        city_dict = pref_dict["city"]
        city = searializeCity(pref_name, city_dict)
        city_list.append(city)
    else:
        for city_dict in pref_dict["city"]:
            city = searializeCity(pref_name, city_dict)
            city_list.append(city)

    # 県
    if len(city_list) > 0:
        pref = Pref(pref_name, city_list)
        return pref
    else:
        return None

# 市の名前から市情報を検索する
def searchCity(city_name):

    # 県情報を取得
    pref_dict_list = getPrefList()

    # 変換
    pref_list = []
    for pref_dict in pref_dict_list:
        pref = serializePref(pref_dict)
        if pref is not None:
            pref_list.append(pref)

    # 対象の市を検索する
    for pref in pref_list:
        for city in pref.city_list:
            if city.name == city_name:
                return city

    return None

# main
if __name__ == "__main__":

    ############

    try:
        starttime = datetime.now()

        # 県情報を取得
        pref_dict_list = getPrefList()

        # 変換
        pref_list = []
        for pref_dict in pref_dict_list:
            pref = serializePref(pref_dict)
            if pref is not None:
                pref_list.append(pref)
                print "県: " + pref.name
                for city in pref.city_list:
                    print "市: " + city.name

        endtime = datetime.now()

        print "success! get time: {0}sec".format((endtime-starttime).seconds)

    except Exception as e:
        print "exception! get: {0}".format(e)

    ############

    try:
        starttime = datetime.now()

        # 市情報を検索
        city = searchCity("大阪")

        endtime = datetime.now()

        if city:
            print city.pref_name
            print city.name
            print city.city_id
            print "success! search time: {0}sec".format((endtime-starttime).seconds)
        else:
            print "failure! search time: {0}sec".format((endtime-starttime).seconds)

    except Exception as e:
        print "exception! search: {0}".format(e)
