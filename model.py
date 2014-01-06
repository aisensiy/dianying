from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy.dialects.mysql import TINYINT
from constants import *
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 10

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registered_at = db.Column(db.DateTime)
    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    is_registered = db.Column(db.Boolean, default=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    src_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dst_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, default=None)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    mid = db.Column(db.Integer)
    type = db.Column(TINYINT)
    param = db.Column(db.Text)
    is_latest = db.Column(TINYINT)

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(255))
    uid = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=datetime.utcnow)
    access_token = db.Column(db.String(255))

class Greeting(db.Model):
    __tablename__ = 'greetings'
    id = db.Column(db.Integer, primary_key=True)
    src_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dst_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_friend = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_friend_at = db.Column(db.DateTime, default=None)

class LastRead(db.Model):
    __tablename__ = 'last_read'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lastid = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

if __name__ == '__main__':
    manager.run()
