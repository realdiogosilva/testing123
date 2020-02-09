from flask import Flask, render_template, request, redirect, Response
from functools import wraps
import psycopg2
import psycopg2.extras
import datetime
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ssl
import urllib.request

app = Flask(__name__)

connection_string = os.environ['DATABASE_URL']

def check_auth(username, password):
    '''THIS IS FOR THE USERNAME AND PASSWORD VARIABLE'''
    return username == os.environ['USERNAME']; password == os.environ['PASSWORD'];

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def mainidea():
    return render_template('HOME.html')

@app.route('/home')
@requires_auth
def hello_world():
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM temperature ORDER BY reading_date DESC LIMIT 5")
        records = cursor.fetchall()

        cursor.execute("SELECT * FROM temperature ORDER BY temperature DESC LIMIT 1 ")
        highest = cursor.fetchall()
        max = highest[0]

        cursor.execute("SELECT * FROM temperature ORDER BY temperature ASC LIMIT 1")
        lowest = cursor.fetchall()
        low = lowest[0]

        return render_template('index.html', temperature=36, records=records, highest=max, lowest=low)

@app.route('/handle',methods=['POST'])
@requires_auth
def handle():
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    amount = float(request.form['amount'])
    location = str(request.form['location'])
    current_date = datetime.datetime.now()
    weekdays = datetime.datetime.now().strftime('%A')
    query = "INSERT INTO temperature(famount, reading_date, locations, weekday) VALUES (%s, %s, %s, %s)"
    val = (amount, current_date, location, weekdays)
    cursor.execute(query, val)
    conn.commit()
    conn.close()
    return redirect('/home')

@app.route('/deletedatabase',methods=['POST'])
@requires_auth
def deletedatabase():
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    amount = float(request.form['amount'])
    query = 'DELETE FROM temperature WHERE famount=(%s)'
    val = (amount)
    cursor.execute(query, val)
    conn.commit()
    conn.close()
    return redirect('/home')


@app.template_filter('format_date')
def reverse_filter(record_date):
    return record_date.strftime('%A %d/%m')

if __name__ == '__main__':
    app.run()
