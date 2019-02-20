import os
import sqlite3
from flask import Flask, g
from views import views
from key import SECRET_KEY 


app = Flask(__name__)

configuration = dict(
    DATABASE=os.path.join(app.root_path, 'mindmaps.db'),
    SECRET_KEY=SECRET_KEY,
    USERNAME='admin',
    PASSWORD='default',
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/received/images/'), # split it into user subfolders
    STATIC_URL_PATH = os.path.join(app.root_path, 'static')

)

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(configuration)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.register_blueprint(views)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(configuration['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_object(table, **kwargs):
    sql = "SELECT * FROM {table} WHERE ".format(table=table)
    for column, condition in kwargs.items():
        sql += str(column) + '=' + '\'' + str(condition) + '\''
    cursor = get_cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def get_cursor():
    """Returns SQlite cursor. """
    cursor = get_db().cursor()
    return cursor


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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder():
    return app.config['UPLOAD_FOLDER']

