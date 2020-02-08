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
    return render_template('base.html')
