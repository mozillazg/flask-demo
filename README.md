
## init

```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
python -c "from demo import run; run.create_db()"
```

## run

```
python -m demo.run
```
