#-*- coding:utf-8 -*-
import os
from flask import Flask, g, request, jsonify, session, url_for, redirect, abort, make_response
from sqlalchemy.orm import joinedload, aliased
from flask_oauthlib.client import OAuth
from cors import crossdomain
from constants import *
import json
from helper import *
from exception import *
from model import User, Message, Movie, db, Account, Greeting
from functools import wraps

app = Flask(__name__)
app.secret_key = r"A0Zr98j/3yX R~XHH!jmN'LWX/,?RT"

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

@app.errorhandler(InvalidParam)
@app.errorhandler(NoAccess)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found(error=None):
    return make_response(jsonify({ 'status': 'error', 'message': 'Not found' }), 404)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kvargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'fail',
                'message': 'not login'
            })
        return f(*args, **kvargs)
    return decorated

# @app.errorhandler(400)
# def bad_request(error=None):
#     print error
#     return make_response(jsonify( { 'status': 'error', 'message': error.message } ), 400)
#
#======================================================================

@app.route('/')
@crossdomain(origin='*')
def index():
    # if 'oauth_token' in session:
    #     access_token = session['oauth_token'][0]
    #     resp = weibo.get('statuses/home_timeline.json')
    #     return jsonify(resp.data)
    resp = make_response(file('README.md').read(), 200)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp


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
      If the user is not registered before, add username for it.
    If not, create and return it.
    """
    try:
        access_token = request.form.get('access_token')
    except Exception as e:
        raise InvalidParam('invalid access_token', status_code=400)

    try:
        token_info = get_token_info(access_token)
        uid = token_info['uid']
        account = db.session.query(Account)\
                  .filter(Account.uid==uid)\
                  .filter(Account.provider=='weibo').first()
        user_info = get_user_info(access_token, uid)
        username = user_info['screen_name']

        if not account: # if this account not found in db create it and its user
            user = User(username=username, registered_at=sqlnow())
            user.accounts = [Account(provider='weibo', access_token=access_token, uid=uid)]
            db.session.add(user)
            db.session.commit()
            account = user.accounts[0]
        else:
            user = account.user
            if not user.is_registered: # if this account is created not by the owner, then created it
                account.username = username
                user.is_registered = True
                user.registered_at = sqlnow()
                db.session.add(user)
                db.session.commit()

        session['user_id'] = account.user_id
        return jsonify({
            'user_id': account.user_id,
            'uid': account.uid
        })

    except Exception as e:
        raise InvalidParam(e.message)

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
        raise InvalidParam('limit or offset is not valid')

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
# @require_auth
def apimessages():
    # this is for dev
    src_user_id = request.args.get('src_user_id')
    if not src_user_id:
        src_user_id = request.form.get('src_user_id')
    if not src_user_id:
        src_user_id = session.get('src_user_id')
    if not src_user_id:
        raise InvalidParam('no src_user_id')
    # dev end
    if request.method == 'POST':
        try:
            user_id = int(request.form.get('user_id'))
            content = request.form['content']
        except:
            raise InvalidParam('invalid user_id or content')

        post_message(src_user_id, user_id, content)
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
        try:
            limit = int(request.args.get('limit', 10))
            offset = int(request.args.get('offset', 0))
        except:
            raise InvalidParam('limit or offset is invalid')

        try:
            user_id = int(request.args.get('user_id'))
        except:
            raise InvalidParam('user_id is invalid')

        items = get_messages(src_user_id, user_id, limit, offset)
        return jsonify({
            "status": "success",
            "data": {
                "items": items
            }
        })

@app.route('/api/friends', methods=['GET'])
@crossdomain(origin='*')
# @require_auth
def apifriends():
    # this is for dev
    src_user_id = request.args.get('src_user_id')
    if not src_user_id:
        src_user_id = session.get('user_id')
    if not src_user_id:
        raise InvalidParam('no src_user_id')
    # dev end
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except:
        raise InvalidParam('limit or offset is not valid')

    from_table = aliased(Greeting)
    to_table = aliased(Greeting)

    friends = db.session.query(from_table.dst_user_id, Account.uid, Account.provider)\
                        .join(to_table, to_table.src_user_id==from_table.dst_user_id)\
                        .join(Account, Account.user_id==from_table.dst_user_id)\
                        .filter(from_table.src_user_id==src_user_id)\
                        .filter(to_table.dst_user_id==from_table.src_user_id)\
                        .order_by(from_table.created_at.desc())\
                        .limit(limit).offset(offset).all()

    return jsonify({
        "status": "success",
        "data": {
            "items": [dict(zip(['user_id', 'uid', 'provider'], [id, uid, provider])) for id, uid, provider in friends]
        }
    })


@app.route('/api/greetings', methods=['GET', 'POST'])
@crossdomain(origin='*')
# @require_auth
def apigreetings():
    # this is for dev
    src_user_id = request.args.get('src_user_id')
    if not src_user_id:
        src_user_id = request.form.get('src_user_id')
    if not src_user_id:
        src_user_id = session.get('src_user_id')
    if not src_user_id:
        raise InvalidParam('no src_user_id')
    # dev end
    if request.method == 'POST': # create greeting
        provider = request.form.get('provider')
        uid = request.form.get('uid')

        if not provider or not uid:
            raise InvalidParam('provider or uid is not invalid')

        account = db.session.query(Account)\
                  .filter(Account.uid==uid)\
                  .filter(Account.provider==provider).first()

        # if the user you are greeting to is not registered in our app then we create
        # a mock user account for him
        if not account:
            user = User()
            user.accounts = [Account(provider=provider, uid=uid)]
            db.session.add(user)
            db.session.commit()
            account = user.accounts[0]

        greeting = db.session.query(Greeting)\
                   .filter(Greeting.src_user_id==src_user_id)\
                   .filter(Greeting.dst_user_id==account.user_id).first()

        if not greeting:
            greeting = Greeting(src_user_id=src_user_id, dst_user_id=account.user_id)
            db.session.add(greeting)
            db.session.commit()

        back_greeting = db.session.query(Greeting)\
                        .filter(Greeting.src_user_id==account.user_id)\
                        .filter(Greeting.dst_user_id==src_user_id).first()

        if back_greeting:
            return jsonify({'status': 'success', 'is_friend': True})
        else:
            return jsonify({'status': 'success', 'is_friend': False})

    else:
        try:
            weibo = request.args.get('weibo').split(',')
        except:
            raise InvalidParam('weibo params is not valid')

        uids = db.session.query(Account.uid)\
               .join(Greeting, Greeting.dst_user_id==Account.user_id)\
               .filter(Greeting.src_user_id==src_user_id)\
               .filter(Account.uid.in_(weibo)).all()

        return jsonify({
            'status': 'success',
            'data': {
                'items': {
                    'weibo': [row[0] for row in uids]
                }
            }
        })


if os.environ.get('SERVER_SOFTWARE', None):
    from bae.core.wsgi import WSGIApplication
    application = WSGIApplication(app)
else:
    app.run(host='0.0.0.0', debug=True)
