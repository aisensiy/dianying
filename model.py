from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy.dialects.mysql import TINYINT
from constants import *
from datetime import datetime
from sqlalchemy import exc, event
from sqlalchemy.pool import Pool


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_STRING
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = -1

@event.listens_for(Pool, "checkout")
def check_connection(dbapi_con, con_record, con_proxy):
    '''Listener for Pool checkout events that pings every connection before using.
    Implements pessimistic disconnect handling strategy. See also:
    http://docs.sqlalchemy.org/en/rel_0_8/core/pooling.html#disconnect-handling-pessimistic'''

    cursor = dbapi_con.cursor()
    try:
        cursor.execute("SELECT 1")  # could also be dbapi_con.ping(),
                                    # not sure what is better
    except exc.OperationalError, ex:
        if ex.args[0] in (2006,   # MySQL server has gone away
                          2013,   # Lost connection to MySQL server during query
                          2055):  # Lost connection to MySQL server at '%s', system error: %d
            # caught by pool, which will retry with a new connection
            raise exc.DisconnectionError()
        else:
            raise

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

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    src_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dst_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    mid = db.Column(db.Integer)
    type = db.Column(TINYINT)
    param = db.Column(db.Text)
    is_latest = db.Column(TINYINT)

if __name__ == '__main__':
    manager.run()
