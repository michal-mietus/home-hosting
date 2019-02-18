import os
import sqlite3
from flask import Flask, g, render_template, request
app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'mindmaps.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def main():
    return 'Main Page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur = get_coursor()
        sql = "SELECT * FROM users WHERE username='{username}'".format(username=request.form['username'])
        cur.execute(sql)
        # all rows
        print(cur.fetchall())

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password-confirm']:
            error = 'Passwords are not the same!'
        elif is_user_created(request.form['username']):
            error = 'User with this username already exists!'
        else:
            

    return render_template('register.html', error=error)


def is_user_created(username):
    sql = "SELECT * FROM users WHERE username='{username}'".format(username=username])
    coursor = get_coursor()
    coursor.execute(sql)
    if coursor.fetchall():
        return True
    return False



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


def get_coursor():
    """Returns SQlite coursor. """
    coursor = get_db().coursor()
    return coursor


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
