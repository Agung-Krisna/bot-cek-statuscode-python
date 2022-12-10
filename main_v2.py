#!/usr/bin/env python3
import requests
import os
import json
from random import randint
from time import sleep
import random
import traceback
import time
from urllib.parse import quote

def agent():
    agents = random.choice(open("useragent.txt", 'r').readlines()).replace("\n", "")
    return agents


useragent = {"User-Agent": agent()}  #{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
sleep_time2 = 30

creds = open('creds.json')
credentials = json.load(creds)

def screenshot_page(copy_domain):
    #192.168.1.1 example ip
    requests.get(f"http://192.168.1.1:8080/screenshot/{copy_domain}")
    print(x.text)
    pass

def telegram_bot_sendtext(bot_message, v1=True):
    bot_token = credentials["bot-token"]
    bot_chatID = credentials["bot-chat-id"]
    if (v1):
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message + '&disable_notification=true'
    else:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=MarkdownV2&text=' + bot_message + '&disable_notification=true'
    result = requests.get(send_text)
    print(result)

if (os.path.exists("monitor.json")):
    previous_monitor = open("monitor.json")
    domain_dict = json.load(previous_monitor)
else:
    domain_dict = {}

def check_status(url, param_timeout=5):
    global useragent
    useragent = {"User-Agent": agent()}
    copy_domain = url.replace("https://","")
    try:
        status_code = requests.get(url, timeout=param_timeout, headers=useragent).status_code
        if (status_code != 200):
            #screenshot_page(copy_domain)
            telegram_bot_sendtext(f"bot mendapatkan status code {status_code} ketika mengecek domain {copy_domain}. Pengecekan ulang akan dilakukan dalam {sleep_time2} detik")
            sleep(randint(1,sleep_time2))
            status_code = requests.get(url, timeout=param_timeout, headers=useragent).status_code
            if (status_code == 200):
                telegram_bot_sendtext(f"pengecekan berhasil status code adalah {status_code}")
    except Exception as e:
        status_code = 0
        telegram_bot_sendtext(f"bot mengalami error ketika mengecek status code\nDetail Error:```\n{e}\n``` ", v1=False)
        print(e)
    return status_code

def sanitize_input(domain):
    if ("http" not in domain):
        domain = "https://" + domain
    domain = domain.replace("\n", "")
    domain = domain.strip(" ")
    return domain


domains = open("domain.txt", 'r').readlines()

def iterateDomains(domains, sleep_time=3, timeout=10):
    for domain in domains:
        copy_domain = domain
        domain = sanitize_input(domain)
        sleep(randint(1,sleep_time))
        status_code = check_status(domain, timeout)
        if (domain in domain_dict):
            if (domain_dict[domain] != status_code):
                status_changed = f"domain {copy_domain} status changed from previous {domain_dict[domain]} into {status_code}"
                telegram_bot_sendtext(status_changed) # doesn't work ?
                print(status_changed)
        if (status_code == 200):
            message_status_code = (f"domain {copy_domain} is up")
            print(message_status_code)
        else:
            message_status_code_down = f"domain {copy_domain} is down, status code = {status_code}"
            telegram_bot_sendtext(message_status_code_down) # this also doesn't work
            print(message_status_code_down)
        domain_dict[domain] = status_code
    
    json_f = json.dumps(domain_dict)
    json_file = open("monitor.json", "w")
    json_file.write(json_f)
    json_file.close()


print("script mulai berjalan")  #telegram_bot_sendtext_untuk_agungsurya("script mulai berjalan") #telegram_bot_sendtext("script mulai berjalan")
start = time.time()
iterateDomains(domains)
end = time.time()

time_required = round(end - start)

print(f"script telah selesai berjalan, waktu berjalan:  {time_required} sekon")   #telegram_bot_sendtext_untuk_agungsurya(f"script telah selesai berjalan, waktu berjalan:  {time_required} sekon") #telegram_bot_sendtext(f"script telah selesai berjalan, waktu berjalan:  {time_required} sekon")
# print(f"program telah selesai dengan waktu {time_required} sekon")
