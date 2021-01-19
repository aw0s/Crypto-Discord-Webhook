import requests
from json import loads
from time import sleep

from euro_scraper import get_euro


webhook_url = '' # Insert link to your Discord webhook here.

while True:
    data_text = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=pln&order=market_cap_desc&per_page=100&page=1&sparkline=false').text
    data = loads(data_text)

    euro_value_pln = get_euro()

    btc_pln = round(data[0]['current_price'])
    btc_euro = round(btc_pln / euro_value_pln)
    eth_pln = round(data[1]['current_price'])
    eth_euro = round(eth_pln / euro_value_pln)

    data = {
        'username': 'Crypto Webhook',
        'embeds': [
            {
                'title': 'BTC and ETH values',
                'description': 'Cryptocurrencies values:',
                'color': 0x00ff00,
                'fields': [
                    {
                        'name': 'Bitcoin',
                        'value': f'{btc_euro} euro\n{btc_pln} pln',
                    },
                    {
                        'name': 'Ethereum',
                        'value': f'{eth_euro} euro\n{eth_pln} pln',
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

    sleep(30)
