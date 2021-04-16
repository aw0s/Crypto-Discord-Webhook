#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from json import loads
from time import sleep

import requests
from dotenv import load_dotenv


load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


def get_currency_price(currency: str) -> float:
    data_nbp_text = requests.get('http://api.nbp.pl/api/exchangerates/tables/a?format=json').text
    data_nbp = loads(data_nbp_text)

    if currency == 'euro':
        euro_in_pln = float(data_nbp.get(0).get('rates').get(7).get('mid'))
        return euro_in_pln
    elif currency == 'dollar':
        dollars_in_pln = float(data_nbp.get(0).get('rates').get(1).get('mid'))
        return dollars_in_pln


def main():

    while True:
        data_text = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=pln&order=market_cap_desc&per_page=100&page=1&sparkline=false').text
        data = loads(data_text)

        date_and_hour = datetime.now().strftime('%d/%m/%Y %H:%m')

        euro_value_pln = get_currency_price('euro')
        dollar_value_pln = get_currency_price('dollar')

        btc_pln = round(data[0]['current_price'])
        btc_euro = round(btc_pln / euro_value_pln)
        btc_dollar = round(btc_pln / dollar_value_pln)

        eth_pln = round(data[1]['current_price'])
        eth_euro = round(eth_pln / euro_value_pln)
        eth_dollar = round(eth_pln / dollar_value_pln)
        
        data = {
            'username': 'Crypto Webhook',
            'embeds': [
                {
                    'title': 'Cryptocurrencies values',
                    'description': date_and_hour,
                    'color': 0xba34eb,
                    'fields': [
                        {
                            'name': 'Bitcoin',
                            'value': f'{"{:,}".format(btc_dollar)} USD\n{"{:,}".format(btc_euro)} EUR\n{"{:,}".format(btc_pln)} PLN',
                        },
                        {
                            'name': 'Ethereum',
                            'value': f'{"{:,}".format(eth_dollar)} USD\n{"{:,}".format(eth_euro)} EUR\n{"{:,}".format(eth_pln)} PLN',
                        },
                    ],
                    'footer': {
                        'icon_url': 'https://cdn.discordapp.com/attachments/788498507187224577/801006516140113940/7TmLHS1.png',
                        'text': 'Crypto Webhook'
                    },
                },
            ]
        }

        requests.post(
            WEBHOOK_URL,
            json=data,
        )

        sleep(3600)


if __name__ == '__main__':
    main()
