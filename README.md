#twitter client

**This use of virtualenv is always recommended.**

Install dependencies via `pip`:

```
pip install -r requirements.txt
```

Create a `config.py` file in the following format:

```
DEBUG=False
PROXY=False
SECRET_KEY='A required field for flask apps'
TWITTER_CONSUMER_KEY='Get this from twitter'
TWITTER_CONSUMER_SECRET='see above'
```

Note: when `PROXY` is set to true, the entire authorization process will be taken from Twitter to your local server, where the app is deployed.

And, run:

```
python twitter.py
```

The twitter client should then be accessible at port 5000 from any browser, or alternatively you can choose to deploy on SaaS platforms, such as Heroku.
