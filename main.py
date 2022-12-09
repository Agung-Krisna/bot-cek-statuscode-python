#!/usr/bin/env python3
import requests
import os
import json
from random import randint
from time import sleep
import random
import traceback
import time

def agent():
    agents = random.choice(open("/useragent.txt", 'r').readlines()).replace("\n", "")
    #print(agents)
    return agents


useragent = {"User-Agent": agent()}  #{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
sleep_time2 = 30

def telegram_bot_sendtext(bot_message):
    bot_token = ''
    bot_chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=MarkdownV2&text=' + bot_message + '&disable_notification=true'
    requests.get(send_text)

if (os.path.exists("monitor.json")):
    previous_monitor = open("monitor.json")
    domain_dict = json.load(previous_monitor)
else:
    domain_dict = {}

def check_status(url, param_timeout=5):
    global useragent
    useragent = {"User-Agent": agent()}
    try:
        status_code = requests.get(url, timeout=param_timeout, headers=useragent).status_code
        if (status_code != 200):
            #requests.get("https://api.telegram.org/bot/sendMessage?chat_id=?disable_notification=true&text=ststutcde")
            telegram_bot_sendtext(f"bot mendapatkan status code {status_code} melakukan pengecekan ulang dalam {sleep_time2} detik")
            sleep(randint(1,sleep_time2))
            status_code = requests.get(url, timeout=param_timeout, headers=useragent).status_code
    except Exception as e:
        status_code = 0
        telegram_bot_sendtext(f"bot mengalami error ketika mengecek status code\nDetail Error:```\n{e}\n``` ")
        #telegram_bot_sendtext("bot mendapatkn status code" + str(status_code))
        #print(useragent)
    return status_code

def sanitize_input(domain):
    if ("http" not in domain):
        domain = "http://" + domain
    domain = domain.replace("\n", "")
    domain = domain.strip(" ")
    return domain


domains = open("domain2.txt", 'r').readlines()

def iterateDomains(domains, sleep_time=5, timeout=60):
    for domain in domains:
        copy_domain = domain
        domain = sanitize_input(domain)
        sleep(randint(1,sleep_time))
        status_code = check_status(domain, timeout)
        if (domain in domain_dict):
            if (domain_dict[domain] != status_code):
                status_changed = f"domain {copy_domain} status changed from previous {domain_dict[domain]} into {status_code}"
                telegram_bot_sendtext(status_changed)
                print(status_changed)
        if (status_code == 200):
            message_status_code = (f"domain {copy_domain} is up")
            print(message_status_code)
        else:
            message_status_code_down = f"domain {copy_domain} is down, status code = {status_code}"
            telegram_bot_sendtext(message_status_code_down)
            print(message_status_code_down)
        domain_dict[domain] = status_code
    json_f = json.dumps(domain_dict)
    json_file = open("monitor.json", "w")
    json_file.write(json_f)
    json_file.close()
telegram_bot_sendtext("script mulai berjalan")
start = time.time()
iterateDomains(domains)
end = time.time()
telegram_bot_sendtext(f"script telah selesai berjalan, waktu berjalan:  {end - start}")
