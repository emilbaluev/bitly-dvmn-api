import requests
import os
from dotenv import load_dotenv
import argparse
from urllib.parse import urlparse


def get_short_link(token, url_link):
    url = 'https://api-ssl.bitly.com/v4//bitlinks'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    params = {'long_url': url_link}
    response = requests.post(url=url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['link']


def get_total_clicks(headers, base_url, short_link):
    click_url = f'https://api-ssl.bitly.com/v4//bitlinks/{short_link}/clicks/summary'
    params = {'unit': 'day', 'units': '-1'}
    click_response = requests.get(click_url, headers=headers, params=params)
    click_response.raise_for_status()
    return click_response.json()['total_clicks']


def is_bitlink(headers, short_link):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{short_link}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    parser = argparse.ArgumentParser(
        description='Cчитает количество кликов или создает короткую ссылку')
    parser.add_argument('url', help='Ссылка для проверки')
    args = parser.parse_args()
    headers = {'Authorization': f'Bearer {token}'}
    link = args.url
    short_link = urlparse(link).netloc + urlparse(link).path

    try:
        if is_bitlink(headers, short_link):
            total_clicks = get_total_clicks(headers, short_link)
            print(f'По ссылке {link} перешли {total_clicks} раз(а).')
        else:
            bitlink = get_short_link(token, link)
            print(
                'Теперь для доступа к {} воспользуйтесь ссылкой:\n{}'.format(
                    link, bitlink))
    except requests.ConnectionError:
        print('Сайт не отвечает.')
    except KeyError:
        print('Ошибка ввода ссылки')
    except requests.HTTPError:
        print('Ошибка сервиса Bitly')


if __name__ == '__main__':
    main()
