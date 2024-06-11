#!/usr/bin/python
# coding=utf-8

import sys
import sqlite3
import telepot
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
from datetime import date
import traceback
import xml.etree.ElementTree as ET

api_key = 'iM%2B5OYQQSMdcWfhPLplO76%2FH6N49AujG%2FmmOXOanS9NnbU12XeWhcMlNILeAwsn4g9%2FdVBe7ppJECUDKiGGaIw%3D%3D'
baseurl = 'http://apis.data.go.kr/1262000/CountryBasicService/getCountryBasicList?'
warningurl = 'http://apis.data.go.kr/1262000/TravelWarningService/getTravelWarningList?'
banurl = 'http://apis.data.go.kr/1262000/TravelBanService/getTravelBanList?'

def getDataFromAPI(url, params):
    full_url = url + params
    try:
        print(f"Requesting URL: {full_url}")  # 디버그 출력
        res_body = urlopen(full_url).read()
        print(f"Response: {res_body}")  # 디버그 출력
        soup = BeautifulSoup(res_body, 'xml')  # XML 파서 지정
        items = soup.findAll('item')
        res_list = []
        for item in items:
            item_text = re.sub('<.*?>', '|', item.text).strip()
            # 링크 제거
            item_text = re.sub(r'http\S+', '', item_text).strip()
            res_list.append(item_text)
        print(f"Parsed Items: {res_list}")  # 디버그 출력
        return res_list
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return []

def getBasicData(countryname):
    encoded_countryname = quote(countryname)
    params = f'serviceKey={api_key}&countryName={encoded_countryname}'
    return getDataFromAPI(baseurl, params)

def getWarningData(isocode):
    params = f'serviceKey={api_key}&isoCode1={isocode}'
    return getDataFromAPI(warningurl, params)

def getBanData(isocode):
    params = f'serviceKey={api_key}&isoCode1={isocode}'
    return getDataFromAPI(banurl, params)

def sendMessage(user, msg):
    bot = telepot.Bot(TOKEN)
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def getPlanInfo(plan_name):
    tree = ET.parse('plans.xml')
    root = tree.getroot()
    for plan in root.findall('plan'):
        if plan.find('planname').text == plan_name:
            # 일정의 장소 이름만 추출
            schedule = plan.find('schedule')
            day_places = {}
            if schedule is not None:
                for day in schedule:
                    places = [place.get('name') for place in day.findall('place')]
                    day_places[day.tag] = ', '.join(places)

            plan_info = {
                'planname': plan.find('planname').text,
                'startdate': plan.find('startdate').text,
                'enddate': plan.find('enddate').text,
                'plancountry': plan.find('plancountry').text,
                'schedule': day_places,
                'checklist1': plan.find('checklist1').text if plan.find('checklist1') is not None else '',
                'checklist2': plan.find('checklist2').text if plan.find('checklist2') is not None else '',
                'cost': plan.find('cost').text if plan.find('cost') is not None else '',
                'memo': plan.find('memo').text if plan.find('memo') is not None else ''
            }
            return plan_info
    return None

def getAllPlanNames():
    tree = ET.parse('plans.xml')
    root = tree.getroot()
    plan_names = [plan.find('planname').text for plan in root.findall('plan')]
    return plan_names

TOKEN = '7130067605:AAGNwcbgWZKgtGBNsBdhCIthonUEa3Bgscc'

if __name__ == '__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')
    print('[', today, '] received token :', TOKEN)
    bot = telepot.Bot(TOKEN)
    from pprint import pprint
    pprint(bot.getMe())
