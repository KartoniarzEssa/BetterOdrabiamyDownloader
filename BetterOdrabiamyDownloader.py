import click, requests, json, inspect, os.path, getpass, re
from bs4 import BeautifulSoup
from google_play_scraper import app

print('Starymisiada Software ©\nhttps://github.com/KartoniarzEssa/BetterOdrabiamyDownloader\n')

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
save = False
version = app('com.swmansion.dajspisac')['version']

ua = f'new_user_agent-android-{version}-sdk_gphone_x86-26e4068038698964'


def download_page(token, page, bookid):
    print(f'Pobieranie strony {page}...')
    rget = json.loads(requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent': ua,'Authorization': f'Bearer {token}'}).content.decode('utf-8'))
    if not 'data' in rget:
        if not clear_warning(token):
            print('Brak danych strony. Prawdopodobnie masz jakąś blokadę na koncie!')
            exit()
        rget = json.loads(requests.get(url=f'https://odrabiamy.pl/api/v2/exercises/page/premium/{page}/{bookid}', headers={'user-agent': ua,'Authorization': f'Bearer {token}'}).content.decode('utf-8'))
        if not 'data' in rget:
            print('Brak danych strony. Prawdopodobnie masz jakąś blokadę na koncie!')
            exit()
    lists = rget['data']
            
    name = lists[0].get('book').get('name').replace('/','')
    name = name.replace('-','')

    if not os.path.exists(f'{path}/{name}-{bookid}'):
        os.makedirs(f'{path}/{name}-{bookid}/{page}/data')

    for exercise in lists:
        solution = exercise.get("solution")
        soup = BeautifulSoup(solution, 'html.parser')
        videos = exercise['videos']
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
            try:
                data = img['src']
                r = requests.get(data)
                soup.find('img', src=data)['src'] = f'./data/{exc_id}-{img_num}.jpg'
                with open(f'{path}/{name}-{bookid}/{page}/data/{exc_id}-{img_num}.jpg','wb') as f:
                    img_num += 1
                    f.write(r.content)
                    f.close()
            except:
                pass
            
        for expr in soup.find_all('math-expr'):
            if not '\\\\displaystyle' in expr:
                expr['expr'] = expr['expr'].replace('strike(', 'cancel(').replace('strike', 'cancel')
                pattern = r'ul\((?!.*\))'
                expr['expr'] = re.sub(pattern, 'ul', expr['expr'])
            
        with open(f'{path}/{name}-{bookid}/{page}/index.html', 'a+') as file:
            zadanie = ''
            if str(exc_num).isnumeric():
                zadanie = 'Zadanie '
            file.write(f'<a style="color:red; font-size:25px;">{zadanie}{exc_num}</a><br>\n{soup}<br>')
            if videos:
                for video in videos:
                    file.write(f'<p>https://www.youtube.com/watch?v={video["contentId"]}</p><br>\n<iframe src=https://www.youtube.com/embed/{video["contentId"]} height="400" width="600"></iframe>')
            file.close()
    
    with open(f'{path}/{name}-{bookid}/{page}/index.html', 'r+') as file:
        content = file.read()
        file.seek(0, 0)
        file.write("""<!DOCTYPE html>
<head>
<meta charset='UTF-8'>
<style>
    @font-face{font-family:KaTeX_Main fallback;size-adjust:95%;src:local("Times New Roman"),local("LiberationSerif")}@font-face{font-family:KaTeX_Main fallback;size-adjust:83%;src:local("Noto Serif")}:root{--odr-text-decoration-color:currentColor;--odr-math-text-font-family:KaTeX_Main,"KaTeX_Main fallback",serif}.odr-strikethrough{text-decoration-color:var(--odr-text-decoration-color)}.odr-downdiagonalstrike,.odr-updiagonalstrike{-webkit-text-size-adjust:100%;text-size-adjust:100%;display:inline-block;position:relative;white-space:nowrap}.odr-downdiagonalstrike:not(.odr-strikethrough),.odr-updiagonalstrike:not(.odr-strikethrough){text-decoration:none}.odr-downdiagonalstrike:after,.odr-updiagonalstrike:before{bottom:0;content:"";left:0;position:absolute;right:0;top:0}.odr-updiagonalstrike:before{background:linear-gradient(to right bottom,transparent calc(50% - 1px),var(--odr-text-decoration-color) 49.5%,var(--odr-text-decoration-color) 50.5%,transparent calc(50% + 1px))}.odr-downdiagonalstrike:after{background:linear-gradient(to right top,transparent calc(50% - 1px),var(--odr-text-decoration-color) 49.5%,var(--odr-text-decoration-color) 50.5%,transparent calc(50% + 1px))}.odr-updiagonalstrike:before.odr-downdiagonalstrike:after{background:linear-gradient(to right bottom,transparent calc(50% - 1px),var(--odr-text-decoration-color) 49.5%,var(--odr-text-decoration-color) 50.5%,transparent calc(50% + 1px)),linear-gradient(to right top,transparent calc(50% - 1px),var(--odr-text-decoration-color) 49.5%,var(--odr-text-decoration-color) 50.5%,transparent calc(50% + 1px))}.odr-comment,.odr-footnote{font-size:.8333357142857143em}math-expr{font-size:1.15rem}.katex{font-family:var(--odr-math-text-font-family)}.katex-display>.katex{white-space:normal}.katex-html>.base{padding-bottom:.25em;padding-top:.25em} 
</style>
<link href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.css" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.js"></script>
<script src="https://unpkg.com/asciimath2tex@1.2.1/dist/asciimath2tex.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/mhchem.min.js"></script>
<script>
  window.WebFontConfig = {
    custom: {
      families: ['KaTeX_AMS', 'KaTeX_Caligraphic:n4,n7', 'KaTeX_Fraktur:n4,n7',
        'KaTeX_Main:n4,n7,i4,i7', 'KaTeX_Math:i4,i7', 'KaTeX_Script',
        'KaTeX_SansSerif:n4,n7,i4', 'KaTeX_Size1', 'KaTeX_Size2', 'KaTeX_Size3',
        'KaTeX_Size4', 'KaTeX_Typewriter'],
    },
  };
</script>
<script src="https://cdn.jsdelivr.net/npm/webfontloader@1.6.28/webfontloader.js"></script>
<script>
        const parser = new AsciiMathParser();
        document.addEventListener("DOMContentLoaded", function () {
            const mathExprs = document.querySelectorAll('math-expr');
    
            mathExprs.forEach(function (element) {
                var expr = element.getAttribute('expr');
                const span = document.createElement('span');

                if (!expr.includes("\\\\displaystyle")) {
                    var expr = parser.parse(expr);
                }

                katex.render(expr, span, {
                    throwOnError: false,
                });
                
                element.appendChild(span);
            });
        });
</script>
</head>
"""+content)
        file.close()

    try:
        if len(os.listdir(f'{path}/{name}-{bookid}/{page}/data')) == 0:
            os.rmdir(f'{path}/{name}-{bookid}/{page}/data')
    except:
        pass

def get_token(user, password):
    rpost = requests.post(url=('https://odrabiamy.pl/api/v2/sessions'), json=({"login": f"{user}", "password": f"{password}"})).content
    token = json.loads(rpost)
    if not 'data' in token:
        return False
    token = json.loads(rpost)['data']['token']
    user_info = json.loads(requests.get(url='https://odrabiamy.pl/api/v2/users/current_user', headers={'user-agent': ua, 'authorization': f'bearer {token}'}).content.decode('utf-8'))
    if user == user_info['data']['name']:
        return token
    return False
    
def clear_warning(token):
    response = json.loads(requests.get(url='https://odrabiamy.pl/api/v2/users/current_user', headers={'user-agent': ua, 'authorization': f'bearer {token}'}).content.decode('utf-8'))
    if response['data']['userOffences'] != []:
        return False
    if response['data']['blocked'] is False:
        return True
    if 'message' in response['data']['blocked']:
        if response['data']['blocked']['message'] == 'Dziś rozwiązałeś z nami już 60 zadań, przez co osiągnięty został dzienny limit przeglądanych rozwiązań. Możliwość dalszego wyświetlania treści zostanie wznowiona o północy':
            return False
    confirm = json.loads(requests.post(url='https://odrabiamy.pl/api/v2/users/confirm_warning', headers={'user-agent': ua, 'authorization': f'bearer {token}'}).content.decode('utf-8'))
    if confirm['message'] == 'User accepted warning':
        print("""\n
              ========================================
              Usunięto ostrzeżenie o limicie dziennym!
              ========================================
              \n""")
        return True
    return False

if os.path.exists(f'{path}/credentials'):
    file = open(f'{path}/credentials', 'r')

    try:
        load = json.load(file)
        user = load['user']
        password = load['password']
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
            print('Niepoprawny e-mail lub hasło.')
            exit()
else:
    user = input('Podaj E-Mail: ')
    password = getpass.getpass(prompt='Podaj hasło: ')
    save = click.confirm('Zapisać dane logowania?', default=False)
    token = get_token(user, password)
    if token == False:
        print('Niepoprawny e-mail lub hasło.')
        exit()
        
user_info = json.loads(requests.get(url='https://odrabiamy.pl/api/v2/users/current_user', headers={'user-agent': ua, 'authorization': f'bearer {token}'}).content.decode('utf-8'))
if user_info['data']['premiumLevel'] == None:
    print('Nie masz premium, więc ten skrypt nie zadziała!')
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
