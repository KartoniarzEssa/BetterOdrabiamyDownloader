import click, requests, json, inspect, os.path, getpass
from bs4 import BeautifulSoup

print('Starymisiada Software ©\nhttps://github.com/KartoniarzEssa/BetterOdrabiamyDownloader\n')

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
save = False

def download_page(token, page, bookid):
    print(f'Pobieranie strony {page}...')
    rget = requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent':'new_user_agent-huawei-143','Authorization': f'Bearer {token}'}).content.decode('utf-8')
    lists = json.loads(rget).get('data')
    name = lists[0].get('book').get('name').replace('/','')
    name = name.replace('-','')

    if not os.path.exists(f'{path}/{name}-{bookid}'):
        os.makedirs(f'{path}/{name}-{bookid}/{page}/data')

    for exercise in lists:
        solution = exercise.get("solution")
        soup = BeautifulSoup(solution, 'html.parser')
        exc_id = exercise.get('id')
        exc_num = exercise.get('number')
        svg_num = 0
        img_num = 0
        
        for obj in soup.find_all('object', class_='small', type='image/svg+xml'):
            obj.extract()
            
        for obj in soup.find_all('object', class_='math small', type='image/svg+xml'):
            obj.extract()

        if not os.path.exists(f'{path}/{name}-{bookid}/{page}'):
            os.makedirs(f'{path}/{name}-{bookid}/{page}/data')
        
        for svg in soup.find_all(attrs={'type' : 'image/svg+xml'}):
            try:
                data = svg['data']
                r = requests.get(data)
                soup.find('object', data=data)['data'] = f'./data/{exc_id}-{svg_num}.svg'
                with open(f'{path}/{name}-{bookid}/{page}/data/{exc_id}-{svg_num}.svg','wb') as f:
                    svg_num += 1
                    f.write(r.content)
                    f.close()
            except:
                pass
            
        for img in soup.find_all('img'):
            data = img['src']
            try:
                r = requests.get(data)
                soup.find('img', src=data)['src'] = f'./data/{exc_id}-{img_num}.jpg'
                with open(f'{path}/{name}-{bookid}/{page}/data/{exc_id}-{img_num}.jpg','wb') as f:
                    img_num += 1
                    f.write(r.content)
                    f.close()
            except:
                pass

        file = open(f'{path}/{name}-{bookid}/{page}/index.html', 'a+', encoding='utf-8')
        file.write(f'<head><meta charset="UTF-8"></head>\n<a style="color:red; font-size:25px;">Zadanie {exc_num}</a><br>\n{soup}<br>')
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

if save == True:
    credentials = {"user":f"{user}", "password":f"{password}"}
    file = open(f"{path}/credentials", "w")
    json.dump(credentials, file)
    file.close()
        
rget = requests.get(url=f'https://odrabiamy.pl/api/v3/books/{bookid}').content.decode('utf-8')
if json.loads(rget).get('name') == None:
    print('Złe ID książki!')
    exit()

pages = json.loads(rget).get('pages')

start_page = click.prompt('Strona od której chcesz zacząć pobierać\n(Enter = od początku)', type=int, default=pages[0], show_default=False)
end_page = click.prompt('Strona do której chcesz pobierać\n(Enter = do końca)', type=int, default=pages[-1], show_default=False)

name = json.loads(rget).get('name').replace('/','')
for page in pages:
    if not os.path.exists(f'{path}/{name}-{bookid}/{page}'):
        if start_page <= page:
            if end_page >= page:
                download_page(token, page, bookid)
                print(f'Pobrano stronę {page}')
if pages[-1] >= end_page:
    print('Pobrano książkę!')
else:
    print('Podana liczba wykracza poza ilość stron w tej książce!')