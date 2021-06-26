import sqlite3
import os
from datetime import *
import locale

# database creation
cur = os.path.abspath(os.getcwd())
if not os.path.isfile(f'{cur}/db.sqlite'):
    open(f'{cur}/db.sqlite', 'x')
else: pass

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

# date and items for today 
locale.setlocale(locale.LC_ALL, '')
today = datetime.today().strftime('%d-%m-%B').split('-')
print(f'Boas vindas ao terminal todo! Hoje é dia {today[0]} de {today[2]}!')

def init():
    db.execute(f"SELECT dates_id FROM dates WHERE date < ?", (today[0],))
    date1_id = str(db.fetchone()).replace('(', '').replace(')', '').replace(',', '')
    db.execute("DELETE FROM items WHERE dates_id = ?", (date1_id,))
    db.execute('DELETE FROM dates WHERE date < ?', (today[0],))

    db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (today[0],))
    date2_id = str(db.fetchone()).replace('(', '').replace(')', '').replace(',', '')
    db.execute('SELECT item FROM items WHERE dates_id = ?', (date2_id,))
    i = db.fetchall()
    
    if i:
        print('Items para hoje: ')
        for row in range(len(i)):
            sla = str(i[row]).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
            print(f"- {sla}")
    else: print('Sem itens para hoje!')

init()

# functions
def addItem(date, item):
    db.execute(f'SELECT * FROM dates WHERE date = ?', (date,))
    data = db.fetchall()
    
    if len(data) == 0:
        print('Data não encontrada, criando uma nova...')
        db.execute(f"INSERT INTO dates VALUES (NULL, ?)", (date,))
        db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (date,))
        date_id = db.fetchall()[0][0]

        db.execute(f"INSERT INTO items VALUES (?, ?)", (str(date_id), str(item),))
        print(f"Criada data {date}")
    else:
        db.execute(f"SELECT dates_id FROM dates WHERE date = ?", (date,))
        date_id = db.fetchall()[0][0]

        db.execute(f"INSERT INTO items VALUES (?, ?)", (str(date_id), str(item),))
        print(f"Adicionado item a data {date}")

    database.commit()

def doneItem(item):
    def findItem():
        db.execute(f'SELECT * FROM items WHERE item = ?', (item,))
        data = db.fetchall()[0]
        if data: return data
        else: return False
    
    if findItem():
        print(f'Item encontrado! Excluindo item...')
        db.execute('DELETE FROM items WHERE item = ?', (item,))
        print('Item excluído!')
    else: 
        print('Item não encontrado...')
    
    database.commit()
