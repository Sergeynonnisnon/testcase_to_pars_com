# coding=UTF-8
import re
import requests
from bs4 import BeautifulSoup

import sqlite3

from fake_useragent import UserAgent

ua = UserAgent()

class parse_fastest():
    def __init__(self):
        pass

    def get_fast_info(self, list_search, lens=100, number_list=1):
        """
        :param list_search: list to search need to url search zakupki.gov
        :param lens: len records on page in url search
        :param number_list: pagination number list
        :return:{serch_query:{number_contract:name,price,date},...}
        """

        result = {}
        for e in list_search:
            url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&' \
                  'search-filter=+Дате+размещения' \
                  f'&pageNumber={number_list}&sortDirection=false&' \
                  f'recordsPerPage=_{lens}' \
                  '&showLotsInfoHidden=false' \
                  '&sortBy=PUBLISH_DATE' \
                  '&fz44=on' \
                  '&af=on' \
                  '&placingWayList=EA44' \
                  '%2CEAP44%2CEAB44%2CEAO44%2CEEA44%2CZK504%2CZKP504%2CEZK504%2COK504%2COKP504%2COKK504' \
                  '%2COKA504%2CEOK504%2COKB504%2COKI504' \
                  '&selectedLaws=FZ44' \
                  '&currencyIdGeneral=-1' \
                  '&customerPlace=8408974%2C8408975' \
                  '&customerPlaceCodes=91000000000%2C92000000000' \
                  '&OrderPlacementSmallBusinessSubject=on' \
                  '&OrderPlacementRnpData=on' \
                  '&OrderPlacementExecutionRequirement=on' \
                  '&orderPlacement94_0=0' \
                  '&orderPlacement94_1=0' \
                  '&orderPlacement94_2=0'

            response = requests.get(url, headers={'accept': '*/*', 'user-agent': ua.firefox})

            if response.status_code > 200:
                print('bad ' + e)
                continue

            soup = BeautifulSoup(response.text, 'lxml')
            soup = soup.body

            quotes = soup.find_all('div', class_="search-registry-entry-block box-shadow-search-input")
            contract_number = {}

            for i in quotes:

                href = i.find(class_="registry-entry__header-mid__number")
                href = href.find('a')
                href = href.get('href')

                names = i.find(class_='registry-entry__body-value')
                names = names.text
                names = re.sub(r'\s\s', '', names)
                names = re.sub(r'\n', '', names)

                price = i.find(class_='col col d-flex flex-column registry-entry__right-block b-left')

                price = price.find(class_='price-block__value').text
                price = re.sub(r'\s', '', price)
                price = re.sub(r'\n', '', price)

                date = i.find(class_='data-block__value')
                date = date.text
                deadline = i.find_all(class_='data-block__value')
                deadline = deadline[-1].text

                # проверяем на наличие в таблице

                contract_number[href] = [names, price, date]


                a = f'zakupki.gov.ru{href}'
                con = sqlite3.connect('oll.db')
                cur = con.cursor()
                cur.execute('''SELECT con_num FROM oll WHERE con_num = ?''', (a,))

                exists = cur.fetchall()

                if exists == []:
                    cur.execute(
                        '''INSERT INTO oll VALUES (?,?,?,?,?,0)''',
                        (a, names, price, date, deadline))

                    con.commit()
                    con.close()

                else:
                    print(f"contract alredy in table. {a}")

                    con.commit()
                    con.close()
                    continue

            result[e] = contract_number

        return result

