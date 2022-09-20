import requests
from bs4 import BeautifulSoup
import csv
import time

ts_2 = time.strftime("%Y%m%d")
CSV_2 = '{}_djinni.csv'.format(ts_2)
HOST_2 = 'https://djinni.co'
URL_2 = 'https://djinni.co/jobs/keyword-python/?region=UKR&exp_level=1y&english_level=pre&subscription_saved=1'
HEADERS_2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
}

def get_html_2(url, params=''):
    r2 = requests.get(url, headers=HEADERS_2, params=params)
    return r2

def get_content_2(html_2):
    soup = BeautifulSoup(html_2, 'html.parser')
    items_2 = soup.find_all('li', class_='list-jobs__item')
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
    return (vacancy_2)


def save_doc_2(items_2, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['дата', 'вакансія', 'опис вакансії', 'посилання на вакансію', 'компанія', 'посилання на компанію'])
        for item in items_2:
            writer.writerow([item['the_date'], item['job_title'], item['description'], HOST_2+item['link_job'], item['company'], HOST_2+item['link_company']])


html_2 = get_html_2(URL_2)
#print(get_content_2(html_2.text))
save_doc_2(get_content_2(html_2.text), CSV_2)
