# Import
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def initiate_db():
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
  ''')

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS Users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  age INT NOT NULL,
  balance INT NOT NULL
  );
  ''')

  connection.commit()



def get_all_products():
  cursor.execute('SELECT * FROM Products')
  products = cursor.fetchall()

  return products



def insert_products():
  products = [
    ('Продукт 1', 'Описание 1', 100),
    ('Продукт 2', 'Описание 2', 200),
    ('Продукт 3', 'Описание 3', 300),
    ('Продукт 4', 'Описание 4', 400)
  ]

  cursor.executemany('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)', products)

  connection.commit()



def is_included(username):
  count = cursor.execute('SELECT COUNT(*) FROM Users WHERE username=?', (username,)).fetchone()
  return count[0] > 0



def add_users(username, email, age):
  if is_included(username):
    return

  cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                (username, email, age, 1000))

  connection.commit()



if __name__ == '__main__':
  initiate_db()
  # insert_products()
