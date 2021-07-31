import sqlite3

con = sqlite3.connect('example.db')

cur = con.cursor()

sql_query = '''
CREATE TABLE IF NOT EXISTS emails
(contactName text, emailValue text);
'''
cur.execute(sql_query)

sql_query = '''
CREATE TABLE IF NOT EXISTS phones
(contactName text, phoneValue text);
'''
cur.execute(sql_query)
con.commit()
con.close()
