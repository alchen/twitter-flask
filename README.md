#twitter


**This use of virtualenv is always recommended.**

Install dependencies via `pip`:

```
pip install -r requirements.txt
```

Create a `config.py` file in the following format:

```
DEBUG = True
SECRET_KEY = ''
TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''
```

And run!

```
python twitter.py
```

The twitter client will be accessible at port 5000 from any browser.
