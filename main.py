import csv
import requests
from bs4 import BeautifulSoup


def get_all_companies():
    res = requests.get('http://www.alba.co.kr/')
    result = []
    soup = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'id': 'MainSuperBrand'}).find_all('li', {'class': 'impact'})
    for s in soup:
        company = clean_string(s.find('a').find(
            'span', {'class': 'company'}).string)
        link = clean_string(s.find('a').get('href'))
        result.append((company, link))
    return result


def get_one_job(company, link):
    print('company', company, 'link', link)
    jobs = []
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'id': 'NormalInfo'}).find('tbody').find_all('tr', {'class': ''})
    for s in soup:
        place = clean_string(s.find('td', {'class': 'local first'}).get_text())
        title = clean_string(s.find('td', {'class': 'title'}).find(
            'span', {'class': 'company'}).get_text())
        time = clean_string(
            s.find('td', {'class': 'data'}).find('span').get_text())
        pay = clean_string(''.join([x.get_text().strip()
                                    for x in s.find('td', {'class': 'pay'}).find_all('span')]))
        date = clean_string(s.find('td', {'class': 'regDate last'}).get_text())
        jobs.append([place, title, time, pay, date])
    write_csv(company, jobs)


def write_csv(name, jobs):
    file = open(name + '.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['place', 'title', 'time', 'pay', 'date'])
    for job in jobs:
        writer.writerow(job)


def clean_string(string):
    return ' '.join(string.split())


ret = get_all_companies()
print(len(ret))
# for r in ret:
#     print(r)
get_one_job(ret[0][0], ret[0][1])
