from os import getenv
from uuid import uuid4

from bcrypt import hashpw, gensalt, checkpw
from dotenv import load_dotenv
from flask import Flask, make_response, render_template, url_for, request, flash, session, g
from flask_session import Session
from redis import StrictRedis
import datetime as dt
import jwt

from forms import RegistrationForm, LoginForm, PackageForm

load_dotenv()
SESSION_TYPE = 'redis'
REDIS_HOST = getenv('REDIS_HOST')
REDIS_PASS = getenv('REDIS_PASS')
JWT_SECRET = getenv('JWT_SECRET')
try:
    JWT_EXP = int(getenv('JWT_EXP'))
except ValueError:
    JWT_EXP = 30
except TypeError:
    JWT_EXP = 30
db = StrictRedis(host=REDIS_HOST, db=0, port=6379)
SESSION_REDIS = db

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = getenv('SECRET_KEY')
ses = Session(app)


def redirect(url, status=301):
    response = make_response('', status)
    response.headers['Location'] = url
    return response


def user_exists(username):
    return db.hexists(f'user:{username}', 'password')


def verify_user(username, password):
    password = password.encode()
    hashed = db.hget(f'user:{username}', 'password')
    if not hashed:
        return False
    return checkpw(password, hashed)


def generate_tracking_token(package_label, user):
    payload = {
        'iss': 'web-lab auth server',
        'sub': package_label,
        'usr': user,
        'aud': 'web-lab tracking service',
        'exp': dt.datetime.utcnow() + dt.timedelta(seconds=JWT_EXP)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token


def save_user(email, username, password):
    salt = gensalt(5)
    password = password.encode()
    hashed = hashpw(password, salt)
    db.hset(f'user:{username}', 'password', hashed)
    db.hset(f'user:{username}', 'email', email)
    return True


def save_package(username, recipient, mailbox_address, package_size):
    package_label = '_'.join([str(s).replace(' ', '') for s in [recipient, mailbox_address, package_size]])
    package_id = str(uuid4())
    db.hset(f'packages:{username}', package_label, package_id)
    return True


def load_packages_labels(username):
    return [l.decode() for l in db.hkeys(f'packages:{username}')]


@app.before_request
def get_logged_username():
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = username


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sender/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        if not verify_user(form.username.data, form.password.data):
            flash("Invalid username and/or password")
            return redirect(url_for('login'))
        flash(f'Welcome {username}')
        session['username'] = username
        session['logged-at'] = dt.datetime.utcnow()
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/sender/logout', methods=['GET'])
def logout():
    g.user = None
    session.clear()
    response = make_response('', 301)
    response.headers['Location'] = 'http://localhost:8000'
    response.headers['Cache-Control'] = 'no-cache'
    return response


@app.route('/sender/dashboard', methods=['GET', 'POST'])
def dashboard():
    if g.user is None:
        return 'Not authorized', 401
    user = g.user
    form = PackageForm(request.form)
    if request.method == 'POST' and form.validate():
        success = save_package(user, form.recipient.data, form.mailbox_address.data, form.package_size.data)
        return redirect(url_for('dashboard'))
    packages = load_packages_labels(user)
    tokens = {p: generate_tracking_token(p, user).decode() for p in packages}
    return render_template('dashboard.html', tokens=tokens, form=form)


@app.route('/package/<pid>', methods=['GET'])
def get_package(pid):
    token = request.args.get('token')
    if token is None:
        return 'No access token for the package', 401
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithm=['HS256'], audience='web-lab tracking service')
    except jwt.InvalidTokenError as error:
        print(f'Invalid token error "{error}"')
        return 'Invalid access token'
    if pid != payload.get('sub'):
        return 'Not authorized', 401
    return render_template('package_details.html', package=pid, token=token)


@app.route('/delete_package/<pid>', methods=['GET'])
def delete_package(pid):
    if g.user is None:
        return 'Not authorized', 401
    token = request.args.get('token')
    if token is None:
        return 'No access token for the package', 401
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithm=['HS256'], audience='web-lab tracking service')
    except jwt.InvalidTokenError as error:
        print(f'Invalid token error "{error}"')
        return 'Invalid access token'
    if pid != payload.get('sub'):
        return 'Not authorized', 401

    db.hdel(f'packages:{g.user}', pid)

    return redirect(url_for('dashboard'))


@app.route('/sender/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if not user_exists(form.username.data):
            success = save_user(form.email.data, form.username.data, form.password.data)
        else:
            flash(f'User "{form.username.data}" already exists!')
            return render_template("register.html", form=form)
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
