import requests
from bs4 import BeautifulSoup


def get_all_companies():
    res = requests.get('http://www.alba.co.kr/')
    result = []
    soup = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'id': 'MainSuperBrand'}).find_all('li', {'class': 'impact'})
    for s in soup:
        a = s.find('a')
        company = a.find('span', {'class': 'company'}).string.strip()
        link = a.get('href').strip()
        result.append((company, link))
    return result


def get_one_job(company, link):
    print('company', company, 'link', link)
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser').find(
        'div', {'id': 'NormalInfo'}).find('tbody').find_all('tr', {'class': ''})
    for s in soup:
        # print(s)
        place = s.find('td', {'class': 'local first'})
        title = ''
        time = ''
        pay = ''
        date = ''
        print(place, title, time, pay, date)


ret = get_all_companies()
print(len(ret))
# for r in ret:
#     print(r)
get_one_job(ret[0][0], ret[0][1])