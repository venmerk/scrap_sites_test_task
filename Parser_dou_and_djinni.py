import requests
from bs4 import BeautifulSoup
import csv
import time

ts = time.strftime("%Y%m%d")
CSV = '{}_dou_djinni.csv'.format(ts)

URL_1 = 'https://jobs.dou.ua/vacancies/?category=Python&exp=0-1'
HEADERS_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

HOST_2 = 'https://djinni.co'
URL_2 = 'https://djinni.co/jobs/keyword-python/?region=UKR&exp_level=1y&english_level=pre&subscription_saved=1'
HEADERS_2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
}

def get_html_1(url, params=''):
    r1 = requests.get(url, headers=HEADERS_1, params=params)
    return r1

def get_html_2(url, params=''):
    r2 = requests.get(url, headers=HEADERS_2, params=params)
    return r2

def get_content_1(html_1):
    soup_1 = BeautifulSoup(html_1, 'html.parser')
    items_1 = soup_1.find_all('div', class_='vacancy')
    vacancy_1 = []
    for item in items_1:
        vacancy_1.append(
            {
                'the_date': item.find('div', class_='date').get_text(strip=True),
                'job_title': item.find('a', class_='vt').get_text(strip=True),
                'description': item.find('div', class_='sh-info').get_text(strip=True),
                'link_job': item.find('a', class_='vt').get('href'),
                'company': item.find('a', class_='company').get_text(strip=True),
                'link_company': item.find('a', class_='company').get('href')
            }
        )
    return vacancy_1

def get_content_2(html_2):
    soup_2 = BeautifulSoup(html_2, 'html.parser')
    items_2 = soup_2.find_all('li', class_='list-jobs__item')
    vacancy_2 = []
    for item in items_2:
        vacancy_2.append(
            {
                'the_date': item.find('div', class_='text-date pull-right').get_text(strip=True),
                'job_title': item.find('a', class_='profile').get_text(strip=True),
                'description': item.find('div', class_='list-jobs__description').get_text(strip=True),
                'link_job': item.find('a', class_='profile').get('href'),
                'company': item.find('div', class_='list-jobs__details__info').get_text(strip=True),
                'link_company': item.find('a', class_="").get('href')
            }
        )

    return vacancy_2

def save_doc(items_1, items_2,  path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['ДАТА', 'ВАКАНСІЯ', 'ОПИС ВАКАНСІЇ', 'ПОСИЛАННЯ НА ВАКАНСІЮ', 'КОМПАНІЯ', 'ПОСИЛАННЯ НА КОМПАНІЮ'])
        for item in items_1:
            writer.writerow(
                [item['the_date'], item['job_title'], item['description'], item['link_job'], item['company'],
                 item['link_company']])

        for item in items_2:
            writer.writerow([item['the_date'], item['job_title'], item['description'], HOST_2+item['link_job'], item['company'], HOST_2+item['link_company']])


html_1= get_html_1(URL_1)
html_2 = get_html_2(URL_2)
#print(get_content_1(html_1.text))
#print(get_content_2(html_2.text))
save_doc(get_content_1(html_1.text), get_content_2(html_2.text), CSV)