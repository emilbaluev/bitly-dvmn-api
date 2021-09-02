import requests
import os
from dotenv import load_dotenv
import argparse


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


def get_total_clicks(token, base_url, link):
    short_link = link.split('//')[1]
    click_url = f'{base_url}/bitlinks/{short_link}/clicks/summary'
    headers = {"Authorization": f"Bearer {token}", }
    params = (('unit', 'day'), ('units', '-1'),)
    click_response = requests.get(click_url, headers=headers, params=params)
    click_response.raise_for_status()
    return click_response.json()['total_clicks']


def check_bitlink(token, base_url, link):
    bitlink_check_url = f"{base_url}bitlinks/{link}"
    headers = {"Authorization": f"Bearer {token}", }
    response = requests.get(bitlink_check_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = os.getenv("ACCESS_TOKEN")
    base_url = 'https://api-ssl.bitly.com/v4/'
    parser = argparse.ArgumentParser(description='Cчитает количество кликов или создает короткую ссылку')
    parser.add_argument('url', help='Ссылка для проверки')
    args = parser.parse_args()
    link = args.url
    if link.startswith("https://bit.ly"):
        try:
            bitlink_exist = check_bitlink(token, base_url, link)
            if bitlink_exist is False:
                total_clicks = get_total_clicks(token, base_url, link)
                print(f"По ссылке {link} перешли {total_clicks} раз(а).")
        except requests.ConnectionError:
            print("Сайт не отвечает.")
        except KeyError:
            print('Ошибка ввода ссылки')

        except requests.HTTPError:
            print("Ошибка сервиса Bitly")
    else:
        try:
            bitlink = get_short_link(token, base_url, link)
            print(f"Теперь для доступа к {link} Вы можете воспользоваться следующей ссылкой:\n{bitlink}")
        except requests.ConnectionError:
            print("Сайт не отвечает.")
        except KeyError:
            print('Ошибка ввода ссылки')
        except requests.HTTPError:
            print("Ошибка сервиса Bitly")


if __name__ == "__main__":
    main()