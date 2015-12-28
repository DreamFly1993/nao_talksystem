#! /usr/bin/python
# _*_coding=utf-8_*_
# ToDo: get weather info from wthrcdn.etouch.cn

import requests
import json
import time

'''
Example:
{
    "desc":"OK","status":1000,
    "data":{
        "wendu":"1",
        "ganmao":"昼夜温差大，且空气湿度较大，易发生感冒，请注意适当增减衣服，加强自我防护避免感冒。",
        "forecast":[
            {"fengxiang":"无持续风向","fengli":"微风级","high":"高温 3℃","type":"晴","low":"低温 -6℃","date":"28日星期一"},
            {"fengxiang":"无持续风向","fengli":"微风级","high":"高温 4℃","type":"霾","low":"低温 -5℃","date":"29日星期二"},
            {"fengxiang":"无持续风向","fengli":"3-4级","high":"高温 5℃","type":"晴","low":"低温 -6℃","date":"30日星期三"},
            {"fengxiang":"无持续风向","fengli":"微风级","high":"高温 4℃","type":"多云","low":"低温 -5℃","date":"31日星期四"},
            {"fengxiang":"无持续风向","fengli":"微风级","high":"高温 4℃","type":"多云","low":"低温 -4℃","date":"1日星期五"}
        ],
        "yesterday":{
            "fl":"微风",
            "fx":"无持续风向",
            "high":"高温 -2℃",
            "type":"小雪",
            "low":"低温 -7℃",
            "date":"27日星期日"
        },
        "aqi":"136",
        "city":"北京"
    }
}
'''


class GetWeather:
    def __init__(self):
        self.url = 'http://wthrcdn.etouch.cn/weather_mini?city='
        self.city = '海淀'
        self.date = [0]
        self.today = 0
        # 4+1+1 days from from today
        self.max_tate = 4
        print 'get weather from http://wthrcdn.etouch.cn/weather_mini?city='

    def set_date(self, cur_time):
        if not isinstance(cur_time, list):
            print 'sdfsdf'
            return -1
        self.date = cur_time

    def get_weather_data(self):
        if self.city == '':
            return 'city_null'
        if self.today == 0:
            self.today = int(time.strftime("%d", time.localtime()))

        weather_html = requests.get(self.url + self.city).text
        weather_json = json.loads(weather_html)
        weather = weather_json['data']
        print 'City: ' + weather['city']
        for cur_date in self.date:
            if cur_date == -1:
                x = weather["yesterday"]
                print x["date"] + x["fl"] + x["fx"] + x["low"] + '-' + x["high"]
            else:
                x = weather["forecast"][cur_date]
                print x["date"] + x["fengli"] + x["fengxiang"] + x["low"] + '-' + x["high"]


a = GetWeather()
a.set_date([1, 2])
a.get_weather_data()
