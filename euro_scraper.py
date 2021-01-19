import requests


def get_euro() -> float:
    page = requests.get('https://internetowykantor.pl/kurs-euro/').text

    to_find = '<span class="kurs kurs_sprzedazy bem-single-rate-box__item-rate">'
    index = page.find(to_find)

    start_index = index + len(to_find)
    stop_index = index + len(to_find) + 4

    return float(page[start_index:stop_index].replace(',', '.'))
