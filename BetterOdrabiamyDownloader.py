import click
import requests
import json
import inspect
import os.path
import getpass
import random
import time

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
save = False

def download_page(token, page, bookid):
    rget = requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent':'new_user_agent-huawei-142','Authorization': f'Bearer {token}'}).content.decode('utf-8')
    lists = json.loads(rget).get('data')

    name = lists[0].get('book').get('name').replace('/','')

    if not os.path.exists(f'{path}/{name}-{bookid}'):
        os.makedirs(f'{path}/{name}-{bookid}')
        os.makedirs(f'{path}/{name}-{bookid}/{page}')

    for exercise in lists:
        if not os.path.exists(f'{path}/{name}-{bookid}/{page}'):
            os.makedirs(f'{path}/{name}-{bookid}/{page}')
        number = exercise.get('number')
        file = open(f'{path}/{name}-{bookid}/{page}/index.html', 'a+', encoding='utf-8')
        file.write(f'<head><meta charset="UTF-8"></head>\n<a style="color:red; font-size:25px;">Zadanie {number}</a><br>\n{exercise.get("solution")}<br>')
        file.close()

def get_token(user, password):
    try:
        rpost = requests.post(url=('https://odrabiamy.pl/api/v2/sessions'), json=({"login": f"{user}", "password": f"{password}"})).content
        token = json.loads(rpost).get('data').get('token')
        return token
    except:
        return False

if os.path.exists(f'{path}/credentials'):
    file = open(f'{path}/credentials', 'r')
    try:
        load = json.load(file)
        user = load.get('user')
        password = load.get('password')
        file.close()
        token = get_token(user, password)
    except:
        token = False
    if token == False:
        print('Nie udało się pobrać danych logowania z pliku. Wpisz je ręcznie!')
        user = input('Podaj E-Mail: ')
        password = getpass.getpass(prompt='Podaj hasło: ')
        save = click.confirm('Zapisać dane logowania?', default=False)
        token = get_token(user, password)
        if token == False:
            print('Niepoprawny e-mail lub hasło. A może nie masz premium?')
            exit()
else:
    user = input('Podaj E-Mail: ')
    password = getpass.getpass(prompt='Podaj hasło: ')
    save = click.confirm('Zapisać dane logowania?', default=False)
    token = get_token(user, password)
    if token == False:
        print('Niepoprawny e-mail lub hasło. A może nie masz premium?')
        exit()
    
bookid = click.prompt('Podaj ID cionszki', type=int)
start_page = click.prompt('Strona od której chcesz zacząć pobierać\n(Enter = od początku)', type=int, default=0, show_default=False)

if save == True:
    credentials = {"user":f"{user}", "password":f"{password}"}
    file = open(f"{path}/credentials", "w")
    json.dump(credentials, file)
    file.close()
        
rget = requests.get(url=f'https://odrabiamy.pl/api/v1.3/ksiazki/{bookid}').content.decode('utf-8')
if json.loads(rget).get('name') == None:
    print('Złe ID książki!')
    exit()

pages = json.loads(rget).get('pages')
name = json.loads(rget).get('name').replace('/','')
for page in pages:
    if not os.path.exists(f'{path}/{name}-{bookid}/{page}'):
        if start_page <= page:
            seconds = random.randint(2,8)
            download_page(token, page, bookid)
            print(f'Pobrano stronę {page}\nNastępna strona zostanie pobrana za {seconds} sekund')
            time.sleep(seconds)
if pages[-1] >= start_page:
    print('Pobrano książkę!')
else:
    print('Podana liczba wykracza poza ilość stron w tej książce!')