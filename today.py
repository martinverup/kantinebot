import urllib.request
from bs4 import BeautifulSoup
import datetime
import re
import os

link = os.getenv('LINK')

meat_map = {
    "Ko": "🐄",
    "Fisk": "🐟",
    "Kylling": "🐓",
    "Gris": "🐖",
    "Kalkun": "🦃",
    "Kalv": "🐄",
    "Chili": "🌶️",
    "Garlic": "🧄",
    "Alkohol": "🍷",
    "Vildt": "🦌",
    "And": "🦆"
}

def get_key(m):
    return meat_map.get(m.group(1), '')

def map_meat(img_tag):
    pattern = r'<img.+?src="\/Images\/(.+?)\.png".+?\/?>'
    return re.sub(pattern, get_key, str(img_tag))


def get_menu():
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')

    weekdays = soup.find_all('span', {'class': 'auto-style22'})
    weekdays = list(map(lambda x: x.get_text().strip(), weekdays))

    menu = soup.find_all('div', {
                         'style': 'font-size: large; font-weight: 700; font-family: Arial, Helvetica, sans-serif; text-align: center;'})
    menu = list(map(lambda x: BeautifulSoup(
        map_meat(x), 'html.parser').get_text().strip(), menu))
    menu = list(map(lambda x: re.sub(r'[^\S\n]+', ' ', x), menu))

    menu_week = soup.find_all('div',
                             {'style': 'font-size: xx-large; font-weight: 700; font-family: Arial, Helvetica, sans-serif; text-align: center;'})
    menu_week = menu_week[0].get_text().strip()
    menu_week = re.findall('\d+', menu_week)[0]

    weeknumber = datetime.datetime.today().isocalendar().week

    if len(weekdays) >= 5 and len(menu) >= 5 and menu_week == str(weeknumber):
        return dict(zip(weekdays, menu))

    return dict()


weekday = datetime.datetime.today().weekday()

menuplan = get_menu()


if len(menuplan) > weekday:
    menu = list(menuplan.values())[weekday]
    print(menu)
else:
    print('Ingen menuplan i dag')
