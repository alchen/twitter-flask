# Twitter Client

This is a web client designed to proxy requests to Twitter from where direct access is not available.

## Usage

1. Create and fill in the `config.py` file.
2. Install dependencies via `pip` and run:

```
pip install -r requirements.txt
python twitter.py
```

Or, upload this to your SAAS platform of choice.

## Configuration

Create a `config.py` file in the following format:

```
DEBUG=False
PROXY=False
SECRET_KEY='A required field for flask apps'
TWITTER_CONSUMER_KEY='Get this from twitter'
TWITTER_CONSUMER_SECRET='see above'
```

When `PROXY` is set to true, the entire authorization process will be taken from Twitter to your local server, where the app is deployed. This is, of course, an added security risk, but convenient when Twitter cannot be directly accessed.
