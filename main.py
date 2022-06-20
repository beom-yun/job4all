import csv
import requests
from bs4 import BeautifulSoup


def get_all_companies():
    try:
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
    except:
        return None


def get_one_job(company, link):
    try:
        jobs = []
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser').find(
            'div', {'id': 'NormalInfo'}).find('tbody')

        if soup.string == '채용공고가 없습니다.':
            write_csv(company, [])
            return True

        soup = soup.find_all('tr', {'class': ''})
        for s in soup:
            place = clean_string(
                s.find('td', {'class': 'local first'}).get_text())
            title = clean_string(s.find('td', {'class': 'title'}).find(
                'span', {'class': 'company'}).get_text())
            time = clean_string(
                s.find('td', {'class': 'data'}).find('span').get_text())
            pay = clean_string(''.join([x.get_text().strip()
                                        for x in s.find('td', {'class': 'pay'}).find_all('span')]))
            date = clean_string(
                s.find('td', {'class': 'regDate last'}).get_text())
            jobs.append([place, title, time, pay, date])
        write_csv(company, jobs)
        return True
    except:
        print('get one job error')
        return False


def write_csv(name, jobs):
    file = open(f'{check_name(name)}.csv', mode='w')
    writer = csv.writer(file)
    writer.writerow(['place', 'title', 'time', 'pay', 'date'])
    for job in jobs:
        writer.writerow(job)


def check_name(name):
    for ch in ['/', '\\', '?', '*', ':', '|', '"', '<', '>']:
        if ch in name:
            name = name.replace(ch, '_')
    return name


def clean_string(string):
    return ' '.join(string.split())


cnt_success, cnt_failed = 0, 0
ret = get_all_companies()
if not ret:
    print('Request error')
    exit(0)
for i, (company_name, company_link) in enumerate(ret):
    if get_one_job(company_name, company_link):
        print(f'Scrapping {company_name} ... Success!')
        cnt_success += 1
    else:
        print(f'Scrapping {company_name} ... Failed!')
        cnt_failed += 1
print(
    f'total: {len(ret)}, success: {cnt_success}, failed: {cnt_failed} ... Done!')
