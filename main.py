# coding=UTF-8
import datetime
import json
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()
url = 'https://www.eldorado.ru'


class task2():
    def __init__(self):
        self.url = self.get_cat(self.go_to_catalog())

        self.get_product_hrefs(self.url)

    def go_to_catalog(self):
        url = 'https://www.eldorado.ru'
        response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        href = dom.xpath(f"//a[text()='Каталог']")
        url_cat= url + href[0].get('href')
        print(f"go to {url_cat}")
        return url_cat

    def get_cat(self,url):

        response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))

        urls = []
        a = dom.xpath(f"//a[@class='Fj' and contains(text(),'Телевизоры') ]")

        for i in a[:3]:# here is limit link categories
            href = (i.get('href'))

            urls.append('https://www.eldorado.ru' + href)
        print(f"get it categories {urls}")

        return urls


    def get_product_hrefs(self, urls):

        for i in urls:

            url = i

            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})
            if response.status_code > 200:
                print('нет коннекта')
            soup = BeautifulSoup(response.content, "html.parser")
            dom = etree.HTML(str(soup))
            hrefs = dom.xpath(f"//a[@class='ou']")
            urls = []

            for i in hrefs[:3]:# here is limit to links product
                href = (i.get('href'))
                self.task1('https://www.eldorado.ru' + href + '/?show=response#customTabAnchor')



    def pagi_step(self,url):
        """

        :param url: url product
        :return: data review in dict like {'user': user, 'sity': sity, 'userReviewDate': userReviewDate, 'star': star, "review": review,
                    'review_score': review_score}
        """
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

            midleblock = i.find('div', class_='middleBlockItem').text
            midleblock = midleblock.split('                    ', )
            review = midleblock[2]
            review_score = re.sub(r'\s\s', '', midleblock[-1])

            data = {'user': user, 'sity': sity, 'userReviewDate': userReviewDate, 'star': star, "review": review,
                    'review_score': review_score}
            _data_full.append(data)

        return _data_full

    def task1(self, url):
        """
        task№1
        :param url: URL product
        :return: None
        """
        print(url)
        data_full = []
        namefile = int(datetime.datetime.timestamp(datetime.datetime.today()))

        response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

        if response.status_code > 200:
            print('нет коннекта')

        soup = BeautifulSoup(response.text, 'lxml')
        soup = soup.body

        pagi = soup.find_all('a', class_='page')[-1].text

        pagi= int(pagi)

        if pagi == 1:
            for i in self.pagi_step(url):
                data_full.append(i)

        else:

            for page in range(1,pagi):

                print(page, 'list rewew')
                for i in self.pagi_step(url+f'/page/{page}/?show=response'):
                    data_full.append(i)

        with open(f'{namefile}.json', 'w') as f: # create and write json
            json.dump(data_full, f,ensure_ascii=False)
            f.close()

        with open(f'{namefile}.json') as json_file:# read json
            data = json.load(json_file)
            print(f"there are now {len(data)} records of user reviews in the {namefile}.json   product ={url} ")

task2()