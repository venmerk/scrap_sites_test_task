import requests
from bs4 import BeautifulSoup
import csv
import time

ts_1 = time.strftime("%Y%m%d")
CSV_1 = '{}_dou.csv'.format(ts_1)
HOST_1 = ''
URL_1 = 'https://jobs.dou.ua/vacancies/?category=Python&exp=0-1'
HEADERS_1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'
}

def get_html_1(url, params=''):
    r1 = requests.get(url, headers=HEADERS_1, params=params)
    return r1

def get_content_1(html_1):
    soup = BeautifulSoup(html_1, 'html.parser')
    items_1 = soup.find_all('div', class_='vacancy')
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
    return (vacancy_1)


def save_doc_1(items_1, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['дата', 'вакансія', 'опис вакансії', 'посилання на вакансію', 'компанія', 'посилання на компанію'])
        for item in items_1:
            writer.writerow([item['the_date'], item['job_title'], item['description'], item['link_job'], item['company'], item['link_company']])


html_1 = get_html_1(URL_1)
#print(get_content_1(html_1.text))
save_doc_1(get_content_1(html_1.text), CSV_1)