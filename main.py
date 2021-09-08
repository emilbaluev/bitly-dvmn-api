import requests
import os
from dotenv import load_dotenv
import argparse
from urllib.parse import urlparse


def get_short_link(token, base_url, url_link):
    url = f'{base_url}/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    params = {'long_url': url_link}
    response = requests.post(url=url, headers=headers, json=params)
    response.raise_for_status()
    return response.json()['link']


def get_total_clicks(headers, base_url, short_link):
    click_url = f'{base_url}/bitlinks/{short_link}/clicks/summary'
    params = {'unit': 'day', 'units': '-1'}
    click_response = requests.get(click_url, headers=headers, params=params)
    click_response.raise_for_status()
    return click_response.json()['total_clicks']


def is_bitlink(base_url, headers, short_link):
    response = requests.get(
        "{}/bitlinks/{}".format(base_url, short_link),
        headers=headers)
    return response.ok


def check_bitlink(headers, base_url, link):
    bitlink_check_url = f"{base_url}bitlinks/{link}"

    response = requests.get(bitlink_check_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    base_url = 'https://api-ssl.bitly.com/v4/'
    parser = argparse.ArgumentParser(
        description='Cчитает количество кликов или создает короткую ссылку')
    parser.add_argument('url', help='Ссылка для проверки')
    args = parser.parse_args()
    headers = {"Authorization": f"Bearer {token}"}
    link = args.url
    short_link = urlparse(link).netloc + urlparse(link).path

    try:
        if is_bitlink(base_url, headers, short_link):
            bitlink_exist = check_bitlink(headers, base_url, link)
            if bitlink_exist is False:
                total_clicks = get_total_clicks(headers, base_url, short_link)
                print(f"По ссылке {link} перешли {total_clicks} раз(а).")

        else:
            bitlink = get_short_link(token, base_url, link)
            print(
                "Теперь для доступа к {} воспользуйтесь ссылкой:\n{}".format(
                    link, bitlink))
    except requests.ConnectionError:
        print("Сайт не отвечает.")
    except KeyError:
        print('Ошибка ввода ссылки')
    except requests.HTTPError:
        print("Ошибка сервиса Bitly")


if __name__ == "__main__":
    main()
