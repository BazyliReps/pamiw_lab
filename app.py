import re

from flask import Flask, request, make_response, render_template
import requests

app = Flask(__name__)
app.debug = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


PL = 'ĄĆĘŁŃÓŚŹŻ'
pl = 'ąćęłńóśźż'


@app.route('/isvalid/<field>/<value>s')
def isvalid(field, value):
    if field == 'firstname':
        return re.compile(f'[A-Z{PL}][a-z{pl}]+').match(value)
    if field == 'lastname':
        return re.compile(f'[A-Z{PL}][a-z{pl}]+').match(value)
    if field == 'password':
        return re.compile('.{8,}').match(value.strip())
    if field == 'login':
        return re.compile('[a-z]{3,12}').match(value)
    if field == 'sex':
        return value in ('M', 'F')
    if field == 'photo':
        return value is not None
    return False


@app.route('/check_login/<login>', methods=['GET'])
def check(login):
    r = requests.get(f"https://infinite-hamlet-29399.herokuapp.com/check/{login}")
    response = make_response(r.text, r.status_code)
    return response


@app.route('/sender/sign-up')
def sign_up():
    return render_template("sign_up.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
