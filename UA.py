# coding=UTF-8
import re
import datetime

import requests
from bs4 import BeautifulSoup
import json
import lxml
from lxml import etree
from fake_useragent import UserAgent
ua = UserAgent()
url = 'https://www.eldorado.ru/cat/detail/led-televizor-vitjaz-32lh0202//?show=response#customTabAnchor'


def pagi_step(url):
    response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

    if response.status_code > 200:
        print('нет коннекта')

    soup = BeautifulSoup(response.text, 'html5lib')

    quotes = soup.find_all('div', class_="usersReviewsListItemInnerContainer")
    _data_full = []
    for i in quotes:
        user = i.find(class_="userName").text

        sity = i.find(class_='userFrom').text
        userReviewDate = re.sub(r'\s\s', '', i.find(class_='userReviewDate').text)
        star = len(i.find_all(class_='star starFull'))

        midleblock = i.find('div' ,class_='middleBlockItem').text
        midleblock = midleblock.split('                    ',)
        review=midleblock [2]
        review_score = re.sub(r'\s\s', '',midleblock[-1])
        print(review)
        print(review_score)
        data = {'user': user, 'sity': sity, 'userReviewDate': userReviewDate, 'star': star, "review": review,'review_score':review_score}
        _data_full.append(data)
    return _data_full
pagi_step(url)