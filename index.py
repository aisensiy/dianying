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
from model import User, Message, Movie, db, Account, Greeting, LastRead
from functools import wraps
from datetime import datetime
from better_session import ItsdangerousSessionInterface
import logging, sys

app = Flask(__name__)
app.secret_key = r"A0Zr98j/3yX R~XHH!jmN'LWX/,?RT"
app.session_interface = ItsdangerousSessionInterface()

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

@app.errorhandler(500)
def internal_error(error=None):
    return make_response(jsonify({ 'status': 'error', 'message': 'Internal Error' }), 500)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kvargs):
        user_id = session.get('user_id')
        if not user_id:
            raise NoAccess('not login')
        return f(*args, **kvargs)
    return decorated

#======================================================================

# for debug
def set_src_user_id():
    src_user_id = request.args.get('src_user_id')
    if not src_user_id:
        src_user_id = request.form.get('src_user_id')
    if not src_user_id:
        src_user_id = session.get('user_id')
    if not src_user_id:
        raise InvalidParam('no src_user_id')
    return src_user_id

@app.route('/')
@crossdomain(origin='*')
def index():
    resp = make_response(file('README.md').read(), 200)
    resp.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return resp

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
        if os.environ.get('DEBUG', None):
            token_info = {
                'uid': '1313608362',
                'appkey': '123'
            }
        else:
            token_info = get_token_info(access_token)
        uid = token_info['uid']
        appkey = token_info['appkey']
        account = db.session.query(Account)\
                  .filter(Account.uid==uid)\
                  .filter(Account.provider=='weibo').first()
        if os.environ.get('DEBUG', None):
            user_info = {'screen_name': 'aisensiy'}
        else:
            user_info = get_user_info(access_token, uid, appkey)
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

        session.permanent = True
        session['user_id'] = account.user_id
        return jsonify({
            'status': 'success',
            'data': {
                'user_id': account.user_id,
                'uid': account.uid
            }
        })

    except Exception as e:
        raise InvalidParam(e.message)

def getmovies(movie_type, offset, limit):
    """
    Return movie list
    """
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

def get_messages(uid1, uid2, lastid):
    rows = db.session\
            .query(Message.id, Message.content, Message.created_at, Account.uid)\
            .join(Account, Account.user_id == Message.src_user_id)\
            .filter(Message.id > lastid)\
            .filter(Account.provider == 'weibo')\
            .filter(Message.src_user_id.in_([uid1, uid2]))\
            .filter(Message.dst_user_id.in_([uid1, uid2]))\
            .order_by(Message.id.desc()).all()
    items = [dict(zip(['id', 'content', 'created_at', 'uid'], [id, content, totimestamp(created_at), uid]))
            for id, content, created_at, uid in rows]
    items.reverse()
    return items

@app.route('/api/messages', methods=['GET', 'POST'])
@crossdomain(origin='*')
@require_auth
def apimessages():
    # this is for dev
    src_user_id = set_src_user_id()
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
                'created_at': totimestamp(message.created_at)
            }
        })
    else:
        try:
            lastid = int(request.args.get('lastid', 0))
        except:
            raise InvalidParam('invalid lastid')

        try:
            user_id = int(request.args.get('user_id'))
        except:
            raise InvalidParam('user_id is invalid')

        items = get_messages(src_user_id, user_id, lastid)
        return jsonify({
            "status": "success",
            "data": {
                "items": items
            }
        })

@app.route('/api/friends', methods=['GET'])
@crossdomain(origin='*')
@require_auth
def apifriends():
    # this is for dev
    src_user_id = set_src_user_id()
    # dev end

    try:
        lastid = int(request.args.get('lastid', 0))
    except:
        raise InvalidParam('invalid lastid')

    from_table = aliased(Greeting)
    to_table = aliased(Greeting)

    friends = db.session.query(Greeting.id, Greeting.dst_user_id, Account.uid, Account.provider, Greeting.created_at)\
                        .join(Account, Account.user_id == Greeting.dst_user_id)\
                        .filter(Greeting.src_user_id == src_user_id)\
                        .filter(Greeting.is_friend == True)\
                        .filter(Greeting.id > lastid).all()

    return jsonify({
        "status": "success",
        "data": {
            "items": [dict(zip(['id', 'user_id', 'uid', 'provider', 'created_at'], [id, user_id, uid, provider, totimestamp(created_at)]))
                for id, user_id, uid, provider, created_at in friends]
        }
    })

def post_greeting(request, db, src_user_id):
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
        back_greeting.is_friend = True
        back_greeting.is_friend_at = sqlnow()
        greeting.is_friend = True
        greeting.is_friend_at = sqlnow()
        db.session.add(greeting)
        db.session.add(back_greeting)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'data': {
                'is_friend': True,
                'user_id': account.user_id
            }
        })
    else:
        return jsonify({
            'status': 'success',
            'data': {
                'is_friend': False,
                'user_id': account.user_id
            }
        })

def get_greeting(request, db, src_user_id):
    try:
        lastid = int(request.args.get('lastid', 0))
    except:
        raise InvalidParam('invalid lastid')

    rows = db.session.query(
            Account.uid, Greeting.id, Greeting.created_at, Account.user_id, Greeting.is_friend)\
            .join(Greeting, Greeting.dst_user_id==Account.user_id)\
            .filter(Greeting.src_user_id==src_user_id)\
            .filter(Greeting.id > lastid)\
            .order_by(Greeting.is_friend.desc(), Greeting.created_at.desc(), Greeting.is_friend_at.desc())\
            .all()

    return jsonify({
        'status': 'success',
        'data': {
            'items': [dict(zip(
                ['uid', 'id', 'created_at', 'user_id', 'is_friend'],
                [uid, id, totimestamp(created_at), user_id, is_friend]))
                for uid, id, created_at, user_id, is_friend in rows]
        }
    })


@app.route('/api/greetings', methods=['GET', 'POST'])
@crossdomain(origin='*')
@require_auth
def apigreetings():
    # this is for dev
    src_user_id = set_src_user_id()
    # dev end

    if request.method == 'POST': # create greeting
        return post_greeting(request, db, src_user_id)
    else:
        return get_greeting(request, db, src_user_id)

@app.route('/api/unread_messages', methods=['GET'])
@crossdomain(origin='*')
@require_auth
def apiunread():
    # this is for dev
    src_user_id = set_src_user_id()
    # dev end

    rows = db.session\
            .query(Message.id, Message.content, Message.created_at, Account.uid, Message.src_user_id)\
            .join(Account, Account.user_id == Message.src_user_id)\
            .filter(Account.provider == 'weibo')\
            .filter(Message.read_at == None)\
            .filter(Message.dst_user_id == src_user_id)\
            .order_by(Message.id.desc()).all()
    items = [dict(zip(['id', 'content', 'created_at', 'uid', 'user_id'], [id, content, totimestamp(created_at), uid, src_user_id]))
            for id, content, created_at, uid, src_user_id in rows]
    items.reverse()
    return jsonify({
        "status": "success",
        "data": {
            "items": items
        }
    })

def getlastid(owner_id):
    row = db.session.query(LastRead.lastid)\
            .filter(LastRead.owner_id == owner_id).first()
    if not row:
        lastid = 0
    else:
        lastid = row[0]
    return jsonify({
        'status': 'success',
        'data': lastid
    })

def postlastid(owner_id, lastid):
    item = db.session.query(LastRead)\
            .filter(LastRead.owner_id == owner_id)\
            .first()

    if not item:
        item = LastRead(owner_id=owner_id, lastid=lastid)
    else:
        item.lastid = lastid

    db.session.add(item)
    Message.query.filter_by(dst_user_id=owner_id, read_at=None)\
            .filter(Message.id <= lastid)\
            .update({'read_at': sqlnow()})
    db.session.commit()


    return jsonify({
        'status': 'success',
        'data': lastid
    })


@app.route('/api/last_read', methods=['GET', 'POST'])
@crossdomain(origin='*')
@require_auth
def apilast_read():
    # this is for dev
    src_user_id = set_src_user_id()
    # dev end

    if request.method == 'POST':
        try:
            lastid = int(request.form.get('lastid'))
        except:
            raise InvalidParam('invalid lastid')

        return postlastid(src_user_id, lastid)
    else:
        return getlastid(src_user_id)


if os.environ.get('SERVER_SOFTWARE', None):
    from bae.core.wsgi import WSGIApplication
    app.logger.addHandler(logging.StreamHandler(stream=sys.stderr))
    application = WSGIApplication(app)
else:
    app.run(host='0.0.0.0', debug=True)
