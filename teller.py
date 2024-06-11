#!/usr/bin/python
# coding=utf-8

import sys
import time
import telepot
from pprint import pprint
from datetime import date
import noti
from iso_codes import get_iso_code

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text'].strip()
    isocode = get_iso_code(text)

    if text == "여행리스트":
        plan_names = noti.getAllPlanNames()
        if plan_names:
            noti.sendMessage(chat_id, '[여행 계획 목록]')
            for name in plan_names:
                noti.sendMessage(chat_id, name)
        else:
            noti.sendMessage(chat_id, '저장된 여행 계획이 없습니다.')
        return


    plan_info = noti.getPlanInfo(text)
    if plan_info:
        noti.sendMessage(chat_id, '[여행 계획 정보]')
        noti.sendMessage(chat_id, f"여행 이름: {plan_info['planname']}")
        noti.sendMessage(chat_id, f"시작 날짜: {plan_info['startdate']}")
        noti.sendMessage(chat_id, f"종료 날짜: {plan_info['enddate']}")
        noti.sendMessage(chat_id, f"여행 국가: {plan_info['plancountry']}")

        for day, places in plan_info['schedule'].items():
            noti.sendMessage(chat_id, f"{day}: {places}")

        noti.sendMessage(chat_id, f"준비미비 물품: {plan_info['checklist1']}")
        noti.sendMessage(chat_id, f"준비완료 물품: {plan_info['checklist2']}")
        noti.sendMessage(chat_id, f"비용: {plan_info['cost']}")
        noti.sendMessage(chat_id, f"메모: {plan_info['memo']}")
    elif text and isocode:

        basic_data = noti.getBasicData(text)
        print(f"Basic Data: {basic_data}")
        if basic_data:
            noti.sendMessage(chat_id, '[기본 정보]')
            for item in basic_data:
                noti.sendMessage(chat_id, item)
        else:
            noti.sendMessage(chat_id, '기본 정보가 없습니다.')


        warning_data = noti.getWarningData(isocode)
        if warning_data:
            noti.sendMessage(chat_id, '[경보 정보]')
            for item in warning_data:
                noti.sendMessage(chat_id, item)
        else:
            noti.sendMessage(chat_id, '경고 정보가 없습니다.')


        ban_data = noti.getBanData(isocode)
        if ban_data:
            noti.sendMessage(chat_id, '[금지 정보]')
            for item in ban_data:
                noti.sendMessage(chat_id, item)
        else:
            noti.sendMessage(chat_id, '금지 정보가 없습니다.')
    else:
        noti.sendMessage(chat_id, '잘못된 국가 이름입니다.')

today = date.today()
print('[', today, '] received token :', noti.TOKEN)

bot = telepot.Bot(noti.TOKEN)
pprint(bot.getMe())

bot.message_loop(handle)
print('Listening...')

while 1:
    time.sleep(10)
