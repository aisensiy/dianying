#-*- coding:utf-8 -*-
import os
from flask import Flask, g, request, jsonify, session, url_for, redirect, abort, make_response
from flask_oauthlib.client import OAuth
from cors import crossdomain
from constants import *
import json
from helper import *
from model import User, Message, Movie, db, Account

app = Flask(__name__)
app.secret_key = r"A0Zr98j/3yX R~XHH!jmN'LWX/,?RT"
app.debug = True

# oauth = OAuth(app)
#
# weibo = oauth.remote_app(
#     'weibo',
#     consumer_key='1361202271',
#     consumer_secret='4a23560f987896b762f4ec6ddc9fb3f4',
#     request_token_params={'scope': 'email,statuses_to_me_read'},
#     base_url='https://api.weibo.com/2/',
#     authorize_url='https://api.weibo.com/oauth2/authorize',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://api.weibo.com/oauth2/access_token',
#     # since weibo's response is a shit, we need to force parse the content
#     content_type='application/json',
# )

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'status': 'error', 'message': 'Not found' } ), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'status': 'error', 'message': 'Bad request' } ), 400)

@app.route('/')
@crossdomain(origin='*')
def index():
    # if 'oauth_token' in session:
    #     access_token = session['oauth_token'][0]
    #     resp = weibo.get('statuses/home_timeline.json')
    #     return jsonify(resp.data)
    return 'it works'

# @app.route('/login')
# @crossdomain(origin='*')
# def login():
#     return weibo.authorize(callback=url_for('authorized', next=request.args.get('next') or request.referrer or None, _external=True))
#
# @app.route('/logout')
# @crossdomain(origin='*')
# def logout():
#     session.pop('oauth_token', None)
#     return redirect(url_for('index'))

# @app.route('/login/authorized')
# @weibo.authorized_handler
# @crossdomain(origin='*')
# def authorized(resp):
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         ), 403
#     session['oauth_token'] = resp['access_token']
#     user = UserAccount(db).find_or_create_user(resp['uid'], session['oauth_token'])
#     return jsonify(user)

# @weibo.tokengetter
# def get_weibo_oauth_token():
#     return session.get('oauth_token')
#
# def change_weibo_header(uri, headers, body):
#     """Since weibo is a rubbish server, it does not follow the standard,
#     we need to change the authorization header for it."""
#     auth = headers.get('Authorization')
#     if auth:
#         auth = auth.replace('Bearer', 'OAuth2')
#         headers['Authorization'] = auth
#     return uri, headers, body
#
# weibo.pre_request = change_weibo_header

@app.route('/auth/login', methods=['POST'])
@crossdomain(origin='*')
def authlogin():
    """
    If the account is exist, return it.
    If not, create and return it.
    """
    access_token = request.form['access_token']
    print access_token
    if not access_token:
        abort(400)
    try:
        token_info = get_token_info(access_token)
        uid = token_info['uid']
        account = db.session.query(Account)\
                  .filter(Account.uid==uid)\
                  .filter(Account.provider=='weibo').first()
        user_info = get_user_info(access_token, uid)
        username = user_info['screen_name']

        if not account:
            user = User(username=username)
            user.accounts = [Account(provider='weibo', access_token=access_token, uid=uid)]
            db.session.add(user)
            db.session.commit()
            account = user.accounts[0]

        session['user_id'] = account.user_id
        session['account_id'] = account.id
        return jsonify({
            'user_id': account.user_id,
            'uid': account.uid
        })

    except Exception as e:
        print e
        abort(400)

def getmovies(movie_type, offset, limit):
    """
    Return movie list
    """
    print 'run get movies'
    print '=' * 20
    rows = db.session.query(Movie.param).filter(Movie.type==movie_type).filter(Movie.is_latest==1).limit(limit).offset(offset)
    items = [json.loads(r.param) for r in rows]

    return jsonify({
        "status": "success",
        "data": {
            "items": items
        }
    })

@app.route('/api/movies/<movie_type>')
@crossdomain(origin='*')
def moviescoming(movie_type):
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except:
        abort(400)

    if movie_type == 'coming':
        return getmovies(MOVIE_TYPE_PLAYING, offset, limit)
    else:
        return getmovies(MOVIE_TYPE_COMING, offset, limit)

def post_message(src_user_id, dst_user_id, content):
    message = Message(src_user_id=src_user_id, dst_user_id=dst_user_id, content=content)
    db.session.add(message)
    db.session.commit()

def get_messages(uid1, uid2, limit, offset):
    rows = db.session.query(Message.id, Message.content, Message.created_at).filter(Message.src_user_id.in_([uid1, uid2])).filter(Message.dst_user_id.in_([uid1, uid2])).order_by(Message.id.desc()).offset(offset).limit(limit)
    items = [dict(zip(['id', 'content', 'created_at'], [id, content, created_at])) for id, content, created_at in rows]
    items.reverse()
    return items

@app.route('/api/messages', methods=['GET', 'POST'])
@crossdomain(origin='*')
def apimessages():
    if request.method == 'POST':
        session['user_id'] = 1
        post_message(session['user_id'], int(request.form['user_id']), request.form['content'])
        message = db.session.query(Message).order_by(Message.id.desc()).first()
        return jsonify({
            'status': 'success',
            'data': {
                'id': message.id,
                'src_user_id': message.src_user_id,
                'dst_user_id': message.dst_user_id,
                'content': message.content,
                'created_at': message.created_at
            }
        })
    else:
        session['user_id'] = 1
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        items = get_messages(session['user_id'], int(request.args.get('user_id')), limit, offset)
        return jsonify({
            "status": "success",
            "data": {
                "items": items
            }
        })

@app.route('/api/friends', methods=['GET', 'POST'])
@crossdomain(origin='*')
def apifriends():
    """docstring for apifriends"""
    if request.method == 'POST':
        # post_friends
        return 'post friends'
    else:
        # get_friends()
        abort(404)
        return 'get friends'

if os.environ.get('SERVER_SOFTWARE', None):
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
else:
    app.run(host='0.0.0.0')
