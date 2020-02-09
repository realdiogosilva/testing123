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

@app.route('/')
def mainidea():
    return render_template('HOME.html')
