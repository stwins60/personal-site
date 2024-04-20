import logging
from flask import Flask, render_template, request, url_for, redirect, session, make_response
from flask_recaptcha import ReCaptcha
import sqlite3 as sql
from sqlite3 import Error
import mailer
import random
from dotenv import load_dotenv
import os

load_dotenv()

# Configure logging for the Flask application
logging.basicConfig(filename='flask_errors.log', level=logging.ERROR)

app = Flask(__name__)
#create random secret key with 24 characters
app.secret_key = ''.join(random.choice('0123456789ABCDEF') for i in range(24))
recaptcha = ReCaptcha(app=app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True
app.config['FLASK_APP'] = 'app.py'
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = os.getenv('RECAPTCHA_SECRET_KEY')

headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'Set-Cookie': f'JSSESIONID={app.secret_key}'
}
cookies = f'JSSESIONID={app.secret_key}'

@app.route('/', methods=['GET'])
def index():
    request = make_response(render_template('index.html'))
    request.headers = headers
    if 'JSSESIONID' not in request.headers['Set-Cookie']:
        request.set_cookie('JSSESIONID', cookies)
    elif request.status_code != 200:
        request.status_code = 404
        return render_template('index.html', 404)
    else:
        request.status_code = 200
        return request
        
    return request

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        message = request.form['content']

        if recaptcha.verify():
            msg = 'Recaptcha verified'
        else:
            msg = 'Recaptcha failed'

        if message == '':
            resp = make_response(render_template('index.html', error='Please fill in all fields', msg=msg))
            resp.headers = headers
            return resp
        else:
            try:
                if mailer.ValidateEmail(email):
                    subject = 'Message from app'
                    mailer.sendMyEmail('ifagbemi@africantech.dev', 'idrisniyi94@gmail.com', subject, fname, lname, email, message)
                    resp = make_response(render_template('index.html', success='Your message has been sent', msg=msg))
                    resp.headers = headers
                    resp.status_code = 200
                    return resp 
                else:
                    resp = make_response(render_template('index.html', error='Please enter a valid email', msg=msg))
                    resp.headers = headers
                    resp.status_code = 400
                    return resp
            except Error as e:
                logging.error("An error occurred: %s", str(e))  # Log the error
                resp = make_response(render_template('index.html', error='Something went wrong', msg=msg))
                resp.headers = headers
                resp.status_code = 500
                return resp

    return redirect(url_for('index'))
