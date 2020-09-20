# Flask Login Sample

## Getting Started
A sample login with Flask and SQLAlchemy, using Application Factory.

### Prerequisites

### Installing

From the project root:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 init-db.py
```
Setup creates two users:
admin (pwd: admin role: ADMIN - can handle users)
user (pwd: user role: USER - cannot handle users)

## Running

__as app__

```sh
export FLASK_APP=flaskr
flask run
```

__as wsgi server__

```sh
waitress-serve --host localhost --port 8080 --call 'flaskr:create_app'
```
or
```sh
gunicorn --worker-class eventlet -w 1 -b localhost:8080 wsgi
```

## Deployment

As seen above (gunicorn, waitress...)

## Authors 

## License

This project is licensed under the MIT License
