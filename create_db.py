import sqlite3

con = sqlite3.connect('example.db')

cur = con.cursor()
sql_query = '''
CREATE TABLE IF NOT EXISTS emails
(contactName text, emailValue text);
'''
cur.execute(sql_query)
con.commit()
con.close()


'''
1. Создать таблицу phones с полями contactName, phoneValue
2. Реализовать CRUD операции для таблицы phones (/phones/create/, /phones/read/, /phones/update/, /phones/delete/)

*
'''