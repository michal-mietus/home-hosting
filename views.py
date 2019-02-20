import os
from flask import g, render_template, request, session, url_for, flash, redirect, Blueprint
from werkzeug.utils import secure_filename
from view_decorators import login_required, deny_logged
from models import User
import image_hosting

views = Blueprint('views', __name__, template_folder='templates')

@views.route('/')
def main():
    return 'Main Page'


@views.route('/login', methods=['GET', 'POST'])
@deny_logged
def login():
    error = None
    if request.method == 'POST':
        user = User(request.form['username'], request.form['password'])
        if user.is_created() == False:
            error = 'User with this username doesn\'t exists!'
        else:
            session['logged_in'] = True
            flash('You\'re logged in. ')
            return redirect(url_for('.main'))
    return render_template('login.html', error=error)


@views.route('/register', methods=['GET', 'POST'])
@deny_logged
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
            return redirect(url_for('.main'))
    return render_template('register.html', error=error)


@views.route('/user/all', methods=['GET', 'POST'])
@login_required
def users():
    sql = 'SELECT * FROM users'
    cursor = image_hosting.get_cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    return render_template('users.html', users=users)


@views.route('/image/add', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('.' + request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('.' + request.url)
        if file and image_hosting.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(image_hosting.app.config['UPLOAD_FOLDER'], filename))
            return render_template('image_upload_success.html')

    return render_template('image_upload.html')


@views.route('/image/all', methods=['GET', 'POST'])
@login_required
def display_images():
    filenames = []
    for (dirpath, dirnames, files) in os.walk(image_hosting.get_upload_folder()):
        for file in files:
            filename = 'received/images/' + file
            filenames.append(filename)
    return render_template('images_display.html', filenames=filenames)
