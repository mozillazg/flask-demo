
## init

```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
python mamager db upgrade
```

## run

```
python manager.py runserver

python manager.py runserver -h 0.0.0.0 -d
```
