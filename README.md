# home-hosting
Flask application to store mind maps, plans, pictures etc.

## Introduction
This project was created for easy sharing files, 
images from my phone to server, 
which was initially running on Raspberry Pi 3.

## Technologies
* Python 3.6.7
* Flask 1.0.2
* PostgreSQL
 

## Launch

```
git clone https://github.com/michal-mietus/home-hosting.git
cd home-hosting
```

* Create PostgreSQL database.

* Apply PostreSQL database settings to 'app.py' file into POSTGRES variable.

* In application folder you have to create file 'key.py' with your SECRET_KEY variable.

* After setting key and with created database you should run migrations with command:
```
python3 manage.py db init
python3 manage.py db migrate
```

* Finally you can run your application with:

```
export FLASK_APP=app.py
run flask
```
