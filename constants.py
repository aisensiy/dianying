import os

if os.environ.get('SERVER_SOFTWARE', None):
  ENV = 'production'
else:
  ENV = 'development'

dbconfig = {
  "development": {
    'host': 'localhost',
    'user': 'root',
    'passwd': '000000',
    'port': 3306,
    'charset': 'utf8',
    'db': 'dianying'
  },
  "production": {
    'host': 'sqld.duapp.com',
    'user': '4qw35SBiFUkGdwaFw1NKddhi',
    'passwd': 'AHlNGExhvB1NXdGEhYHl2G0HL3X2zqcx',
    'port': 4050,
    'charset': 'utf8',
    'db': 'uIGHoHrxIlBxvJsjLJSp'
  }
}
(MOVIE_TYPE_PLAYING, MOVIE_TYPE_COMING) = range(2)
DB_STRING = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8' % (
    dbconfig[ENV]['user'],
    dbconfig[ENV]['passwd'],
    dbconfig[ENV]['host'],
    dbconfig[ENV]['port'],
    dbconfig[ENV]['db']
)
