import os
import sqlite3
from flask import Flask, g, render_template, request, session, url_for, flash, redirect
from key import SECRET_KEY


app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'mindmaps.db'),
    SECRET_KEY=SECRET_KEY,
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def main():
    return 'Main Page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if get_user(request.form['username']) == False:
            error = 'User with this username doesn\'t exists!'
        else:
            session['logged_in'] = True
            flash('You\'re logged in. ')
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        if request.form['password'] != request.form['password-confirm']:
            error = 'Passwords are not the same!'
        elif user.is_created():
            error = 'User with this username already exists!'
        else:
            user.save()
            session['logged_in'] = True
            flash('You\'re logged in. ')
            return redirect(url_for('main'))
    return render_template('register.html', error=error)


@app.route('/user/all', methods=['GET', 'POST'])
def users():
    sql = 'SELECT * FROM users'
    cursor = get_cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    print(users)
    return render_template('users.html', users=users)


class User:
    class UserAlreadExistsException(Exception): 
        def __str__(self):
            return 'User with that username already exists!'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.table = 'users'

    def save(self):
        if get_object(self.table, **{'username': self.username}) == []:
            sql = "INSERT INTO users (username, password) VALUES (?, ?);"
            db = get_db()  # while inserting have to call db.commit (connection)
            cursor = get_cursor()
            cursor.execute(sql, (self.username, self.password))
            db.commit()  # connection commit
        else:
            return self.UserAlreadExistsException()

    def is_created(self):
        if get_object(self.table, **{'username': self.username}):
            return True
        return False


def get_object(table, **kwargs):
    sql = "SELECT * FROM {table} WHERE ".format(table=table)
    for column, condition in kwargs.items():
        sql += str(column) + '=' + '\'' + str(condition) + '\''
    cursor = get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    """Initialize new database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def get_cursor():
    """Returns SQlite cursor. """
    cursor = get_db().cursor()
    return cursor


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
