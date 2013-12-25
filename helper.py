import time
import urllib2
import urllib
import json
import datetime

def sqlnow():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def totimestamp(dt):
    return int(unix_time(dt)) * 1000

class APIError(StandardError):
    '''
    raise APIError if receiving json message indicating failure.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (
            self.error_code, self.error, self.request)

def _post_weibo_api_call(url, data=None):
    try:
        resp = urllib2.urlopen(url, data=data)
        r = json.loads(resp.read())
        if r.get('error_code', None):
            raise APIError(
                r.get('error_code'), r.get('error', ''), r.get('request', ''))

        return r
    except urllib2.HTTPError, e:
        try:
            r = json.loads(e.read())
        except:
            r = None

        if r.get('error_code', None):
            raise APIError(
                r.get('error_code'), r.get('error', ''), r.get('request', ''))

        raise e

def _get_weibo_api_call(url, data=None):
    try:
        resp = urllib2.urlopen(url + '?' + data)
        r = json.loads(resp.read())
        if r.get('error_code', None):
            raise APIError(
                r.get('error_code'), r.get('error', ''), r.get('request', ''))

        return r
    except urllib2.HTTPError, e:
        try:
            r = json.loads(e.read())
        except:
            r = None

        if r.get('error_code', None):
            raise APIError(
                r.get('error_code'), r.get('error', ''), r.get('request', ''))

        raise e

# http://open.weibo.com/wiki/Oauth2/get_token_info
def get_token_info(access_token):
    url = 'https://api.weibo.com/oauth2/get_token_info'
    data = urllib.urlencode({'access_token': access_token})
    return _post_weibo_api_call(url, data=data)

def get_user_info(access_token, uid, appkey):
    url = 'https://api.weibo.com/2/users/show.json'
    data = urllib.urlencode({'access_token': access_token, 'uid': uid, 'source':appkey})
    return _get_weibo_api_call(url, data=data)

