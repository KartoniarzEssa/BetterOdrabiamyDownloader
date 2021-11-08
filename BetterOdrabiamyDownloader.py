from os import write
import requests
import json
import inspect
import os.path
import getpass
import random
import time

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

user=input('Podaj E-Mail: ')
password=getpass.getpass(prompt='Podaj hasło: ')
bookid=input('Podaj ID cionszki: ')

rpost = requests.post(url=('https://odrabiamy.pl/api/v2/sessions'), json=({"login": f"{user}", "password": f"{password}"})).content
token = json.loads(rpost).get('data').get('token')

def download_page(token, page, bookid):
    rget = requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent':'new_user_agent-huawei-142','Authorization': f'Bearer {token}'}).content.decode('utf-8')
    lists=json.loads(rget).get('data')

    name=lists[0].get('book').get('name')
    if not os.path.exists(f'{path}/{name}'):
        os.makedirs(f'{path}/{name}')
        os.makedirs(f'{path}/{name}/{page}')

    for list in lists:
        if not os.path.exists(f'{path}/{name}/{page}'):
            os.makedirs(f'{path}/{name}/{page}')
        number=list.get('number')
        file=open(f'{path}/{name}/{page}/index.html', 'a+', encoding='utf-8')
        file.write(f'\n<a style="color:red; font-size:25px;">Zadanie {number}</a>\n'+list.get('solution'))
        file.close
        
def download_book(bookid):
    rget = requests.get(url=f'https://odrabiamy.pl/api/v1.3/ksiazki/{bookid}').content.decode('utf-8')
    pages = json.loads(rget).get('pages')
    name = json.loads(rget).get('name')
    for page in pages:
        if not os.path.exists(f'{path}/{name}/{page}'):
            seconds=random.randint(2,8)
            download_page(token=token, page=page, bookid=bookid)
            print(f'Pobrano stronę {page}\nNastępna strona zostanie pobrana za {seconds} sekund')
            time.sleep(seconds)
    print(pages)

download_book(bookid=bookid)