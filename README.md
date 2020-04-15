**Install**

From the project root:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 setup.py
```

**Run** 

__serve localhost only__

```sh
export FLASK_APP=flaskr
flask run
```

__serve as WSGI__

```sh
waitress-serve --host XXX.XXX.XXX.XXX --port YYYY --call 'flaskr:create_app'
```