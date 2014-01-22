# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import cookielib
from threading import Thread
import json
from helper import *
from constants import *
from gzip import GzipFile
from StringIO import StringIO
import re

HOST_URL = 'http://m.douban.com'
DOUBAN_API_URL = 'http://api.douban.com/v2/movie/subject/'

class DoubanMovies:
  def __init__(self):
    self.url = ''

  def openUrl(self):
    cj = cookielib.CookieJar()
    openUrl = urllib2.urlopen(self.url)
    cjHander = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cjHander)
    urllib2.install_opener(opener)

    return openUrl.readlines()

  #tag=p是正在热映的影片id
  #tag=h3是即将上映影片的id
  def getMovieId(self, tag, *args):
    movieStr = ''
    movieId = []
    movieDict= {}

    for html in self.openUrl():
      movieStr += str(html).strip()
    soup = BeautifulSoup(movieStr.strip(''))

    for con in soup.findAll(tag, *args):
      res = BeautifulSoup(str(con))
      movieId.append(str(res.a["href"]).split("/")[-2])

    return movieId


  #正在热映影片ID
  def nowPlaying(self):
    movie_id = []
    for i in range(1, 3):
      url = HOST_URL + '/movie/recent/now?page=' + str(i)
      self.url = url
      for id in self.getMovieId('p'):
        if re.match('^\d+$', id):
          movie_id.append(id)
    return movie_id

  #即将上映影片ID
  def soonPlaying(self):
    movie_id = []
    for i in range(1, 2):
      url = HOST_URL + '/movie/recent/soon?page=' + str(i)
      self.url = url
      for id in self.getMovieId('div', {'class': 'item'}):
        if re.match('^\d+$', id):
          movie_id.append(id)
    return movie_id

  def getMovieInfos(self):
    res_str = ''
    movie_ids = self.nowPlaying()
    for movie_id in movie_ids:
      self.url = DOUBAN_API_URL + str(movie_id)
      try:
        for res in self.openUrl():
          res_str += res
      except:
        print movie_id
    print res_str

  def run(self):
    Thread(target=self.getMovieInfos()).start()#多线程

def fetch(url):
  request = urllib2.Request(url)
  request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36')
  request.add_header('Accept-Encoding', 'gzip,deflate')
  content = None
  try:
    response = urllib2.urlopen(request)
    content = response.read()
    if response.info().getheader('Content-Encoding') \
      and response.info().getheader('Content-Encoding') == 'gzip':
      content = GzipFile(fileobj=StringIO(content)).read()
  except Exception as e:
    pass
  return content

def insert_movie(db, movie_obj):
  db.execute("insert into movies (mid, type, param, is_latest, created_at) values(%s, %s, %s, %s, %s)",
       (movie_obj['mid'], movie_obj['type'], movie_obj['param'], 1, sqlnow()))

def fetch_playing(ids):
  for id in ids:
    url = DOUBAN_API_URL + str(id)
    resp = fetch(url)
    data = json.loads(resp)
    print data['title'].encode('utf8')
    insert_movie(db, {
      "mid": id,
      "type": MOVIE_TYPE_PLAYING,
      "param": resp,
    })

def fetch_coming(ids):
  for id in ids:
    url = DOUBAN_API_URL + str(id)
    resp = fetch(url)
    data = json.loads(resp)
    print data['title'].encode('utf8')
    insert_movie(db, {
      "mid": id,
      "type": MOVIE_TYPE_COMING,
      "param": resp,
    })

def run(db):
  """docstring for run"""
  db.execute('update movies set is_latest = %s', 0)

  doubanmovie_handler = DoubanMovies()

  playing_ids = doubanmovie_handler.nowPlaying()
  print playing_ids
  fetch_playing(playing_ids)

  coming_ids = doubanmovie_handler.soonPlaying()
  print coming_ids
  fetch_coming(coming_ids)

  db.commit()

if __name__ == "__main__":
  from db import MySQL as DB
  db = DB(dbconfig[ENV])
  run(db)

