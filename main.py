from flask import Flask, request

from utils import generate_password as gp, isPhoneValid, isTextValid

app = Flask(__name__)


@app.route('/hello/')
def hello_world():
    return 'Hello, World!'


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


@app.route('/emails/create/')
def create_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    contact_name = request.args['contactName']
    email_value = request.args['Email']

    if isTextValid(contact_name):
        cur = con.cursor()
        sql_query = f'''
        INSERT INTO emails (contactName, emailValue)
        VALUES ('{contact_name}', '{email_value}');
        '''
        cur.execute(sql_query)
        con.commit()
        con.close()
        response_text = 'Email was updated'
    else:
        response_text = 'Invalid name'

    return response_text


@app.route('/emails/read/')
def read_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = '''
    SELECT * FROM emails;
    '''
    cur.execute(sql_query)
    result = cur.fetchall()
    con.close()

    return str(result)


@app.route('/emails/update/')
def update_email():
    import sqlite3

    contact_name = request.args['contactName']
    email_value = request.args['Email']

    if isTextValid(contact_name):
        con = sqlite3.connect('example.db')
        cur = con.cursor()
        sql_query = f'''
        UPDATE emails
        SET emailValue = '{email_value}'
        WHERE contactName = '{contact_name}';
        '''
        cur.execute(sql_query)
        con.commit()
        con.close()
        response_text = 'Email was updated'
    else:
        response_text = 'Invalid name'

    return response_text


@app.route('/emails/delete/')
def delete_email():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = '''
    DELETE FROM emails;
    '''
    cur.execute(sql_query)
    con.commit()
    con.close()

    return 'delete_email'


@app.route('/phones/create/')
def create_phone():
    import sqlite3

    con = sqlite3.connect('example.db')
    contact_name = request.args['contactName']
    phone_value = request.args['phone']

    if not isTextValid(contact_name):
        response_text = 'Invalid name'
    elif not isPhoneValid(phone_value):
        response_text = 'Invalid phone'
    else:
        cur = con.cursor()
        sql_query = f'''
        INSERT INTO phones (contactName, phoneValue)
        VALUES ('{contact_name}', '{phone_value}');
        '''
        cur.execute(sql_query)
        con.commit()
        con.close()
        response_text = 'Phone was created'

    return response_text


@app.route('/phones/read/')
def read_phone():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = '''
    SELECT * FROM phones;
    '''
    cur.execute(sql_query)
    # fetchall - на выходе список кортежей
    result = cur.fetchall()
    con.close()

    return str(result)


@app.route('/phones/update/')
def update_phone():
    import sqlite3

    contact_name = request.args['contactName']
    phone_value = request.args['phone']

    if not isTextValid(contact_name):
        response_text = 'Invalid name'
    elif not isPhoneValid(phone_value):
        response_text = 'Invalid phone'
    else:
        con = sqlite3.connect('example.db')
        cur = con.cursor()
        sql_query = f'''
        UPDATE phones
        SET  phoneValue = '{phone_value}'
        WHERE contactName = '{contact_name}' ;
        '''
        cur.execute(sql_query)
        con.commit()
        con.close()
        response_text = 'Phone was updated'

    return response_text


@app.route('/phones/delete/')
def delete_phone():
    import sqlite3

    con = sqlite3.connect('example.db')
    cur = con.cursor()
    sql_query = '''
    DELETE FROM phones;
    '''
    cur.execute(sql_query)
    con.commit()
    con.close()

    return 'Phone was deleted'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
