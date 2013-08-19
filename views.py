import os
from twitter import app, twitter
from flask import render_template, session, redirect, flash, url_for, request
from flask import send_from_directory


@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/x-icon')


@app.route('/favicon.png')
def favicon_png():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.png', mimetype='image/png')


@app.route('/')
def show_index():
    token = get_twitter_token()
    if not token:
        return render_template('prompt.html')

    if 'max_id' in request.args:
        resp = twitter.get('statuses/home_timeline.json',
                           data={'max_id': request.args['max_id']})
    else:
        resp = twitter.get('statuses/home_timeline.json')

    if resp.status == 200:
        tweets = resp.data
    else:
        tweets = []
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    since_id = max_id = None
    for tweet in tweets:
        if since_id is None or since_id < tweet['id']:
            since_id = tweet['id']
        if max_id is None or max_id > tweet['id']:
            max_id = tweet['id']
    max_id -= 1

    return render_template('timeline.html', tweets=tweets, max_id=max_id,
                           since_id=since_id, endpoint="show_index",
                           endpoint_args={})


@app.route('/~mentions')
def show_mentions():
    token = get_twitter_token()
    if not token:
        return render_template('prompt.html')

    if 'max_id' in request.args:
        resp = twitter.get('statuses/mentions_timeline.json',
                           data={'max_id': request.args['max_id']})
    else:
        resp = twitter.get('statuses/mentions_timeline.json')

    if resp.status == 200:
        tweets = resp.data
    else:
        tweets = []
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    since_id = max_id = None
    for tweet in tweets:
        if since_id is None or since_id < tweet['id']:
            since_id = tweet['id']
        if max_id is None or max_id > tweet['id']:
            max_id = tweet['id']
    max_id -= 1

    return render_template('timeline.html', tweets=tweets, max_id=max_id,
                           since_id=since_id, endpoint="show_mentions",
                           endpoint_args={})


@app.route('/~messages')
def show_messages():
    token = get_twitter_token()
    if not token:
        return render_template('prompt.html')

    resp = twitter.get('direct_messages.json')
    if resp.status == 200:
        messages = resp.data
    else:
        messages = []
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    return render_template('messages.html', messages=messages)


@app.route('/@<name>')
@app.route('/<name>')
def show_user(name):
    if 'max_id' in request.args:
        resp = twitter.get('statuses/user_timeline.json',
                           data={'max_id': request.args['max_id'],
                                 'screen_name': name})
    else:
        resp = twitter.get('statuses/user_timeline.json',
                           data={'screen_name': name})

    if resp.status == 200:
        tweets = resp.data
    else:
        tweets = []
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    since_id = max_id = None
    for tweet in tweets:
        if since_id is None or since_id < tweet['id']:
            since_id = tweet['id']
        if max_id is None or max_id > tweet['id']:
            max_id = tweet['id']
    max_id -= 1

    return render_template('timeline.html', tweets=tweets, max_id=max_id,
                           since_id=since_id, endpoint="show_user",
                           endpoint_args={'name': name})


@app.route('/+update', methods=['GET', 'POST'])
def update():
    resp = twitter.post('statuses/update.json', data={
        'status': request.form['status'],
        'in_reply_to_status_id': request.form['in_reply_to']
    })
    if resp.status == 403:
        flash('Your tweet was too long.')
    else:
        flash('Successfully tweeted your new status')

    return redirect(url_for('show_index'))


@app.route('/-update/<int:id>')
def unupdate(id):
    resp = twitter.post('statuses/destroy/%d.json' % id)
    if resp.status == 403:
        flash('Delete failed.')
    else:
        flash('Successfully deleted your new tweet')

    return redirect(url_for('show_index'))


@app.route('/+retweet/<int:id>')
def retweet(id):
    resp = twitter.post('statuses/retweet/%d.json' % id)
    if resp.status == 403:
        flash('Retweet failed.')
    else:
        flash('Successfully retweeted.')

    return redirect(request.referrer or url_for('show_index'))


@app.route('/-retweet/<int:id>')
def unretweet(id):
    resp = twitter.get('statuses/show/%d.json?include_my_retweet=1' % id)
    if resp.status == 403:
        flash('Unretweet failed.')
    else:
        retweet_id = resp.data['current_user_retweet']['id']
        resp = twitter.post('statuses/destroy/%d.json' % retweet_id)
        if resp.status == 200:
            flash('Successfully unretweeted.')
        else:
            flash('Unretweet failed.')

    return redirect(request.referrer or url_for('show_index'))


@app.route('/+favorite/<int:id>')
def favorite(id):
    resp = twitter.post('favorites/create.json', data={'id': id})
    if resp.status == 403:
        flash('Favorite failed.')
    else:
        flash('Successfully favorited.')

    return redirect(request.referrer or url_for('show_index'))


@app.route('/-favorite/<int:id>')
def unfavorite(id):
    resp = twitter.post('favorites/destroy.json', data={'id': id})
    if resp.status == 403:
        flash('Unfavorite failed.')
    else:
        flash('Successfully unfavorited.')

    return redirect(request.referrer or url_for('show_index'))


@app.route('/~thread/<int:id>')
def thread(id):
    resp = twitter.get('statuses/show.json', data={'id': id})
    if resp.status == 200:
        tweet = resp.data
    else:
        tweet = None
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    if tweet and tweet['in_reply_to_status_id']:
        resp = twitter.get('statuses/show.json',
                           data={'id': tweet['in_reply_to_status_id']})
        if resp.status == 200:
            replied_tweet = resp.data
        else:
            replied_tweet = None
            flash('Unable to load tweets from Twitter. Maybe out of '
                  'API calls or Twitter is overloaded.')

    return render_template('reply.html', id=id, tweet=tweet,
                           replied_tweet=replied_tweet)


@app.route('/+reply/<int:id>')
def reply(id):
    resp = twitter.get('statuses/show.json', data={'id': id})
    if resp.status == 200:
        tweet = resp.data
    else:
        tweet = None
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    return render_template('reply.html', id=id, tweet=tweet)


@app.route('/+quote/<int:id>')
def quote(id):
    resp = twitter.get('statuses/show.json', data={'id': id})
    if resp.status == 200:
        tweet = resp.data
    else:
        tweet = None
        flash('Unable to load tweets from Twitter. Maybe out of '
              'API calls or Twitter is overloaded.')

    return render_template('quote.html', id=id, tweet=tweet)


@app.route('/login')
def login():
    return twitter.authorize(
        callback=url_for(
            'oauth_authorized',
            next=request.args.get('next') or request.referrer or None
        )
    )


@app.route('/logout')
def logout():
    next_url = request.args.get('next') or url_for('show_index')
    session.pop('twitter_token')

    return redirect(next_url)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('show_index')
    if resp is None:
        flash(u'You have been denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (resp['oauth_token'],
                                resp['oauth_token_secret'])
    session['twitter_user'] = resp['screen_name']
    session['twitter_id'] = resp['user_id']

    icon = twitter.get('users/show.json?screen_name=%s' % resp['screen_name'])
    if icon.status == 200:
        session['twitter_name'] = icon.data['name']
        session['twitter_icon'] = icon.data['profile_image_url']

    return redirect(next_url)
