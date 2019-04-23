import urllib.request
from bs4 import BeautifulSoup
import datetime
from slacker import Slacker
from time import sleep
from tinydb import TinyDB, Query
import yaml
import re
import os

db = TinyDB('./data/db.json')

with open('./data/config.yml') as f:
    config = yaml.safe_load(f)

def get_key(m):
    mapping = config['config']['mapping']
    return mapping.get(m.group(1), '')

def map_meat(img_tag):
    pattern = r'<img.+?src="\/Images\/(.+?)\.png".+?\/?>'
    return re.sub(pattern, get_key, str(img_tag))

def get_menu():
    link = config['config']['menuplan']['link']

    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')

    weekdays = soup.find_all('span', {'class': 'auto-style22'})
    weekdays = list(map(lambda x: x.get_text().strip(), weekdays))

    menu = soup.find_all('div', {'style': 'font-size: large; font-weight: 700; font-family: Arial, Helvetica, sans-serif; text-align: center;'})
    menu = list(map(lambda x: BeautifulSoup(map_meat(x), 'html.parser').get_text().strip(), menu))
    menu = list(map(lambda x: re.sub(r'[^\S\n]+', ' ', x), menu))

    menuplan = dict()

    if len(weekdays) >= 5 and len(menu) >= 5:
        menuplan = dict(zip(weekdays, menu))
        
    return menuplan

def do_sleep():
    if not 'ONCE' in os.environ:
        sleep(config['config']['sleep'])
        return True
    return False

weekday = datetime.datetime.today().weekday()

slack = Slacker(config['config']['slack']['token'])
channel = config['config']['slack']['channel']
icon = config['config']['slack']['icon']

while(True):
    now = datetime.datetime.now()

    if now.hour > 11:
        break

    menuplan = get_menu()

    today = now.strftime('%Y-%m-%d')

    saved = db.search(Query()[today])

    if weekday == 0 and not len(saved):
        for index, day in enumerate(menuplan):
            menu = menuplan[day]
            if menu:
                message = str('*' + day + '*\n' + menu)
                slack.chat.post_message(channel, message, icon_emoji=icon)
            if index == 0:
                db.insert({today: menu})
        continue

    if weekday < 5:
        menu = list(menuplan.values())[weekday]
        if menu:
            
            if len(saved):
                if saved[-1][today] == menu:
                    do_sleep()
                    continue
                else:
                    slack.chat.post_message(channel, '_Menu opdateret:_', icon_emoji=icon)

            message = '*' + list(menuplan.keys())[weekday] + '*\n' + menu
            slack.chat.post_message(channel, message, icon_emoji=icon)
            db.insert({today: menu})
    
    if not do_sleep():
        break
