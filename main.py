from flask import Flask, request

from datetime import datetime
from utils import generate_password as gp

app = Flask(__name__)


@app.route('/hello/')
def hello_world():
    return 'Hello, World!'


'''
CRUD
C - create - /emails/create/ - INSERT INTO ...
R - read - /emails/read/ - SELECT * FROM ...
U - update - /emails/update/ - UPDATE ... SET ...
D - delete - /emails/delete/ - DELETE FROM ...
'''


# a = 1  # [0, 1, 2, 3, 5]
#
# # if a == 1 or a == 2 or a == 3:
# if a in [1, 2, 3, 5]:
#     pass


@app.route('/generate-password/')
def generate_password():
    # validate password-len from client
    password_len = request.args.get('password-len')

    if not password_len:
        password_len = 10
    else:
        if password_len.isdigit():
            password_len = int(password_len)
            # 10 .. 100
        else:
            password_len = 10
            # return 'Invalid parameter password-len. Should be int.'

    password = gp(password_len)
    return f'{password}\n'


@app.route('/requirements/')
def requirements():
    # open and return content
    # read_requirements_txt()
    return 'Hello, World!'


@app.route('/generate-users/')
def generate_users():
    # utils.generate_users()
    return


# @app.route('/generate-password2/')
# def generate_password2():
#     import random
#     import string
#     choices = string.ascii_letters + string.digits + '#$%^'
#     result = ''
#
#     for _ in range(10):
#         result += random.choice(choices)
#
#     return f'{result}\n'

@app.route('/emails/create/')
def create_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    # http://127.0.0.1:5000/emails/create/?contactName=Alex&Email=awdaw@mail.com
    contact_name = request.args['contactName']
    email_value = request.args['Email']

    cur = con.cursor()
    sql_query = f'''
    INSERT INTO emails (contactName, emailValue)
    VALUES ('{contact_name}', '{email_value}');
    '''
    cur.execute(sql_query)
    con.commit()
    con.close()
    return 'create_email'


@app.route('/emails/read/')
def read_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = f'''
    SELECT * FROM emails;
    '''
    cur.execute(sql_query)
    result = cur.fetchall()
    con.close()
    return str(result)


@app.route('/emails/update/')
def update_email():
    import sqlite3

    # http://127.0.0.1:5000/emails/update/?contactName=Alex&Email=awdaw@mail.com

    contact_name = request.args['contactName']
    email_value = request.args['Email']

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = f'''
    UPDATE emails
    SET contactName = '{contact_name}'
    WHERE emailValue = '{email_value}';
    '''
    cur.execute(sql_query)
    con.commit()
    con.close()
    return 'update_email'


@app.route('/emails/delete/')
def delete_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = f'''
    DELETE FROM emails;
    '''
    cur.execute(sql_query)
    con.commit()
    con.close()
    return 'delete_email'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

"""
http://google.com:443/search/?name=hillel&city=Dnepr

1. Protocol
http:// - protocol (https)
ftp:// - file transfer protocol
smtp:// - simple mail transfer protocol
ws:// (wss)

2. Domain (IPv4, IPv6)
google.com, facebook.com, lms.hillel.com
developer.mozilla.org -> 99.86.4.33 (DNS)

0-255.0-255.0-255.0-255
192.172.0.1

# WRONG
192.172.0
192.172.0.1.2
256.192.1.1

localhost -> 127.0.0.1

3. Port
http - 80
https - 443
smtp - 22

5000+

0 - 65535

4. Path
/generate-password/ -> generate_password()
/search/ -> make_search()

5. Query parameters
? - sep
name=hillel&city=Dnepr - 
{'name': 'hillel', 'city': 'Dnepr'}
"""
