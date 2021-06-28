import sqlite3
import os
from datetime import *
import locale
import shutil

# date and welcome
locale.setlocale(locale.LC_ALL, '')
today = datetime.today().strftime('%d-%m-%B').split('-')
print(f'Boas vindas ao terminal todo! Hoje é dia {today[0]} de {today[2]}!')

## useful functions
# convert tuple to string
def toString(tuple):
    if type(tuple) == str:
        return tuple.replace('(', '').replace(')', '').replace(',', '').replace("'", "")
    else: 
        return str(tuple).replace('(', '').replace(')', '').replace(',', '').replace("'", "")

# convert date words to numbers
def toDate(date):
    td = [['today', 'hoje', 'hj'], ['amanha', 'amanhã', 'amnh', 'tomorrow'], ['semana que vem']]
    if date in td[0]:
        date = today[0]
    elif date in td[1]:
        date = str(int(today[0]) + 1)
    elif date in td[2]:
        date = str(int(today[0]) + 7)

    return date

def toNotDate(date):
    if date == today[0]:                    return 'hoje'
    elif date == str(int(today[0]) + 1):    return 'amanhã'
    elif date == str(int(today[0]) + 7):    return 'semana que vem'
    else:                                   return date

# database creation
cur = os.path.abspath(os.getcwd())
if not os.path.isfile(f'{cur}/db.sqlite'):
    open(f'{cur}/db.sqlite', 'x')
else: pass

# database setup
database = sqlite3.connect('db.sqlite')
db = database.cursor()
db.execute("""CREATE TABLE IF NOT EXISTS dates (
    dates_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT
);""")
db.execute("""CREATE TABLE IF NOT EXISTS items (
    dates_id INTEGER,
    item TEXT
);""")

# database for done items
if not os.path.isfile(f'{cur}/itemsdone.sqlite'):
    open(f'{cur}/itemsdone.sqlite', 'x')
else: pass

_database = sqlite3.connect('itemsdone.sqlite')
_db = _database.cursor()
_db.execute('CREATE TABLE IF NOT EXISTS done (date TEXT, item TEXT)')

# function for adding items do done db
def doneDatabase(date, item):
    if date and item:
        _db.execute('INSERT INTO done VALUES (?, ?)', (date.replace("'", ''), str(item),))
        _database.commit()
    else: return 0

# init function
def init():
    # delete todos from dates before today
    db.execute(f"SELECT dates_id FROM dates WHERE date < ?", (today[0],))
    date1_id = toString(db.fetchone())
    db.execute("DELETE FROM items WHERE dates_id = ?", (date1_id,))
    db.execute('DELETE FROM dates WHERE date < ?', (today[0],))
    database.commit()

    # print all todos for today
    db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (today[0],))
    date2_id = toString(db.fetchone())
    db.execute('SELECT item FROM items WHERE dates_id = ?', (date2_id,))
    i = db.fetchall()
    
    if i:
        print('Items para hoje: ')
        for row in range(len(i)):
            sla = toString(i[row])
            print(f"- {sla}")

    else: print('Sem itens para hoje!')

init()

## functions
# add item to database
def addItem(dater, item):
    date = toDate(dater)

    db.execute(f'SELECT * FROM dates WHERE date = ?', (date,))
    data = db.fetchall()
    
    if len(data) == 0:
        print('Data não encontrada, criando uma nova...')
        db.execute(f"INSERT INTO dates VALUES (NULL, ?)", (date,))
        db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (date,))
        date_id = db.fetchall()[0][0]

        db.execute(f"INSERT INTO items VALUES (?, ?)", (str(date_id), str(item),))
        print(f"Item adicionado, criada data {date}")
    else:
        db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (date,))
        date_id = db.fetchall()[0][0]

        db.execute(f"INSERT INTO items VALUES (?, ?)", (str(date_id), str(item),))
        print(f"Adicionado item a data {date}")

    database.commit()

# done item - basically remove item from database
def doneItem(item):
    db.execute(f'SELECT * FROM items WHERE item = ?', (item,))
    data = db.fetchall()[0]
    if data: 
        print(f'Item encontrado! Excluindo item...')
        db.execute('SELECT dates_id FROM items WHERE item = ?', (item,))
        date_id = db.fetchone()[0]
        db.execute('SELECT date FROM dates WHERE dates_id = ?', (date_id,))
        dat = toString(db.fetchone())
        doneDatabase(dat, item)

        db.execute('DELETE FROM items WHERE item = ?', (item,))
        print('Item excluído!')
    else: 
        print('Item não encontrado...')
        
    database.commit()

# show all todos from specific date
def showItems(dater):

    date = toDate(dater)
    db.execute('SELECT dates_id FROM dates WHERE date = ?', (date,))
    row = db.fetchall()
    if row: 
        print(f'Itens para {toNotDate(date)}:\n')
        list = toString(row[0])
        db.execute('SELECT item FROM items WHERE dates_id = ?', (list,))
        item = db.fetchall()
        for i in range(len(item)):
            _item = toString(item[i])
            print(f"- {_item}")
    else: print('Data não existente')

# show all todos and their date
def showAll():
    db.execute('SELECT dates_id FROM dates')
    d = db.fetchall()
    if d:
        for i in range(len(d)):
            list = d[i][0]
            db.execute('SELECT date FROM dates WHERE dates_id = ?', str(list,))
            date = toString(db.fetchone())
            print(f"\nTodos do dia {toNotDate(date)}:")

            db.execute('SELECT item FROM items WHERE dates_id = ?', str(list,))
            it = db.fetchall()
            for row in range(len(it)):
                list = toString(it[row])
                print(f"- {list}")
    else:
        print('Ainda não há nenhum item!')

# show all done todos
def showDone():
    _db.execute('SELECT date FROM done')
    daate = _db.fetchall()

    def parseDuplicated():
        lista = []
        for i in range(len(daate)):
            lista.append(toString(daate[i]))

        return list(dict.fromkeys(lista))
    
    _date = parseDuplicated()

    for i in range(len(_date)):
        _db.execute("SELECT item FROM done WHERE date = ?", (str(_date[i]),))
        _item = _db.fetchall()

        print(f'\nItems feitos de {toNotDate(_date[i])}')
        for row in range(len(_item)):
            itt = toString(_item[row])

            print(f"- {itt}")

# reset entire aplication to default
def resetDefault():
    os.remove(f'{cur}/db.sqlite')
    os.remove(f'{cur}/itemsdone.sqlite')
    shutil.rmtree(f'{cur}/__pycache__', ignore_errors=True)
    