import json
import click
import inspect
import os.path
filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

var1 = input('Cycki dupa wielka kupa: ')
var2 = input('Chuj cie to interesuje kto mi w dupie dzis pakuje: ')

if not os.path.exists(f'{path}/credentials'):
    var3 =  click.confirm('Zapisać dane?', default=False)



#OPCJA 1 ZAPIS
dict1 = {"var1":f"{var1}", "var2":f"{var2}"}
file = open("credentials", "w")
json.dump(dict1, file)

#OPCJA 1 ODCZYT
file = open("credentials", "r")
load = json.load('credentials')
print(load.get('var1'))
print(load.get('var2'))


#OPCJA 2 ZAPIS
#file = open('credentials', 'w')
#file.write(f'{var1}\n{var2}')
#file.close()

#OPCJA 2 ODCZYT
#file = open('credentials', 'r')
#line=file.readlines()
#print(line[0])
#print(line[1])