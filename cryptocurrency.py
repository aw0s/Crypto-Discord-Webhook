#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from json import loads
from time import sleep
from datetime import datetime


def get_currency_price(currency: str) -> float:
    data_nbp_text = requests.get('http://api.nbp.pl/api/exchangerates/tables/a?format=json').text
    data_nbp = loads(data_nbp_text)

    if currency == 'euro':
        euro_in_pln = float(data_nbp[0]['rates'][7]['mid'])
        return euro_in_pln
    elif currency == 'dollar':
        dollars_in_pln = float(data_nbp[0]['rates'][1]['mid'])
        return dollars_in_pln


def main():
    webhook_url = ''  # Insert link to your Discord webhook here.

    while True:
        data_text = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=pln&order=market_cap_desc&per_page=100&page=1&sparkline=false').text
        data = loads(data_text)

        euro_value_pln = get_currency_price('euro')
        dollar_value_pln = get_currency_price('dollar')

        btc_pln = round(data[0]['current_price'])
        btc_euro = round(btc_pln / euro_value_pln)
        btc_dollar = round(btc_pln / dollar_value_pln)

        eth_pln = round(data[1]['current_price'])
        eth_euro = round(eth_pln / euro_value_pln)
        eth_dollar = round(eth_pln / dollar_value_pln)
        
        date_and_hour = datetime.now().strftime('%d/%m/%Y %H:%m')
        
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
                            'value': f'{btc_dollar} dollars\n{btc_euro} euro\n{btc_pln} pln',
                        },
                        {
                            'name': 'Ethereum',
                            'value': f'{eth_dollar} dollars\n{eth_euro} euro\n{eth_pln} pln',
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
            webhook_url,
            json=data,
        )

        sleep(3600)


if __name__ == '__main__':
    main()