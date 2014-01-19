Go to github for this [README](https://github.com/aisensiy/dianying/blob/master/README.md).

## APIS

* GET   /api/movies/(coming|playing)
* GET   /api/unread_messages -- require login
* GET   /api/messages -- require login
* POST  /api/messages -- require login
* GET   /api/last_read -- require login
* POST  /api/last_read -- require login
* GET   /api/friends -- require login
* GET   /api/greetings -- require login
* POST  /api/greetings -- require login
* POST  /auth/login

## 开发模式

在开发模式下，所有需要登录的地方都可以无视。然后所有需要从当前 session 里面去用户 id 的情况都可以传递一个 `src_user_id` 替代之。

例如 `POST /api/greetings` 这个接口可以通过

    curl -d 'uid=123&provider=weibo&src_user_id=1' http://yiqikandianying.duapp.com/api/greetings

搞定

再来一个例子 `POST /api/messages`

    curl -d 'user_id=2&content=bla&src_user_id=1' http://yiqikandianying.duapp.com/api/messages

还有，很多地方都用到了 `user_id`，但是做客户端开发的同学未必有查看数据库的权限，所以没办法知道这个 `user_id` 那做的时候呢可以通过 `POST /api/greetings` 这个接口搞定。因为这个接口的策略是 *如果你打招呼的这个人还没有注册，那么就会给它生成一个账号* 因此这个请求会给你返回这个用户的 `user_id` 的。那么这样你就可以自己创建一些账号做测试了。

## 错误处理

我感觉返回的 `message` 是给开发者的，所以都是简单的说明

### 未登录

http code: 403

```
{
  "message": "not login",
  "status": "fail"
}
```

### 请求参数错误

http code: 400

```
{
  "message": "no src_user_id",
  "status": "error"
}
```

在 `/auth/login` 中可能有微博 api 相关问题导致的报错

http code: 400

```
{
  "message": "Oauth Error: token_rejected:: token =123",
  "status": "error"
}
```

## POST /auth/login

如果这个用户是第一次授权连接我们的应用，那么就会为他建立一个新的账号。否则就返回他的账号。其中 `uid` 是微博账号的 `id` 而 `user_id` 是我们为他创建的账号id。在其他地方使用到的 `user_id` 都是指这个账号。

### paramters:

* access_token: string

### return

```
{
  "status": "success",
  "data": {
    "uid": "1313608362",
    "user_id": 3
  }
}
```

## GET /api/movies/(coming|playing)

### parameters:

* limit: int
* offset: int

### return

```
{
  "data": {
    "items": [
      {
        "alt": "http://movie.douban.com/subject/3793783/",
        "casts": [
          {
            "alt": "http://movie.douban.com/celebrity/1022003/",
            "avatars": {
              "large": "http://img3.douban.com/img/celebrity/large/6760.jpg",
              "medium": "http://img3.douban.com/img/celebrity/medium/6760.jpg",
              "small": "http://img3.douban.com/img/celebrity/small/6760.jpg"
            },
            "id": "1022003",
            "name": "\u6851\u5fb7\u62c9\u00b7\u5e03\u6d1b\u514b"
          },
          {
            "alt": "http://movie.douban.com/celebrity/1054433/",
            "avatars": {
              "large": "http://img3.douban.com/img/celebrity/large/552.jpg",
              "medium": "http://img3.douban.com/img/celebrity/medium/552.jpg",
              "small": "http://img3.douban.com/img/celebrity/small/552.jpg"
            },
            "id": "1054433",
            "name": "\u4e54\u6cbb\u00b7\u514b\u9c81\u5c3c"
          }
        ],
        "collect_count": 86844,
        "comments_count": 44248,
        "countries": [
          "\u7f8e\u56fd"
        ],
        "current_season": null,
        "directors": [
          {
            "alt": "http://movie.douban.com/celebrity/1036409/",
            "avatars": {
              "large": "http://img3.douban.com/img/celebrity/large/1362388356.65.jpg",
              "medium": "http://img3.douban.com/img/celebrity/medium/1362388356.65.jpg",
              "small": "http://img3.douban.com/img/celebrity/small/1362388356.65.jpg"
            },
            "id": "1036409",
            "name": "\u963f\u65b9\u7d22\u00b7\u5361\u9686"
          }
        ],
        "do_count": null,
        "douban_site": "",
        "episodes_count": null,
        "genres": [
          "\u5267\u60c5",
          "\u79d1\u5e7b",
          "\u60ca\u609a"
        ],
        "id": "3793783",
        "images": {
          "large": "http://img3.douban.com/view/movie_poster_cover/lpst/public/p2159078612.jpg",
          "medium": "http://img3.douban.com/view/movie_poster_cover/spst/public/p2159078612.jpg",
          "small": "http://img3.douban.com/view/movie_poster_cover/ipst/public/p2159078612.jpg"
        },
        "mobile_url": "http://movie.douban.com/subject/3793783/mobile",
        "original_title": "Gravity",
        "rating": {
          "average": 8,
          "max": 10,
          "min": 0,
          "stars": "40"
        },
        "ratings_count": 77664,
        "reviews_count": 1011,
        "schedule_url": "http://movie.douban.com/subject/3793783/cinema/",
        "seasons_count": null,
        "subtype": "movie",
        "summary": "bla",
        "title": "\u5730\u5fc3\u5f15\u529b",
        "wish_count": 38680,
        "year": "2013"
      }
    ]
  },
  "status": "success"
}
```

## GET /api/unread_messages

返回当前用户所有没有读取的信息

### parameters:

no parameter

### return:

```
{
  "data": {
    "items": [
      {
        "uid": "123",
        "user_id": 3,
        "content": "test",
        "created_at": 1387348724306
        "id": 7
      },
      {
        "uid": "123",
        "user_id": 3,
        "content": "test",
        "created_at": 1387348724306
        "id": 8
      },
      {
        "uid": "471231231",
        "user_id": 3,
        "content": "test",
        "created_at": 1387348724306
        "id": 9
      }
    ]
  },
  "status": "success"
}
```

## GET /api/messages

### parameters:

* user_id: int
* lastid: int, default: 0

### return:

```
{
  "data": {
    "items": [
      {
        "uid": "123",
        "content": "test",
        "created_at": 1387348724306
        "id": 7
      },
      {
        "uid": "123",
        "content": "test",
        "created_at": 1387348724306
        "id": 8
      },
      {
        "uid": "471231231",
        "content": "test",
        "created_at": 1387348724306
        "id": 9
      }
    ]
  },
  "status": "success"
}
```

## POST /api/messages

### parameters:

* user_id: int
* content: string

### return

```
{
  "data": {
    "id": 14,
    "src_user_id": 1,
    "dst_user_id": 1,
    "content": "test",
    "created_at": 1387348804000
  },
  "status": "success"
}
```

## GET /api/last_read

获取当前用户上次最后获取消息的最大 id

### parameters:

无

### returns:

```
{
  "data" 19,
  "status": "success"
}
```

## POST /api/last_read

设置用户最后查看的消息的最大 `id`，下次请求 `unread_messages` 请求的时候将获取大于 `lastid` 的数据。

### parameters:

* lastid: int

### returns:

```
{
  "data": 19,
  "status": "success"
}
```

## GET /api/friends

返回相互打过招呼的好友列表

### parameters:

* lastid: 返回时间戳大于 `lastid` 的好友, default: 0。

### return

```
{
  "data": {
    "items": [
      {
        "id": 4,
        "created_at": 1387348804000,
        "provider": "weibo",
        "uid": "1313608362",
        "user_id": 3
      }
    ]
  },
  "status": "success"
}
```

## GET /api/greetings

返回已经打过招呼了的 uid。

### parameters:

* lastid: 返回时间戳大于 `lastid` 的打招呼的内容。

### return

返回已经打过招呼的 uid 列表，如果已经是好友关系，那么参数 `is_friend` == `true`。
排序按照 is_friend desc, created_at desc

```
{
  "data": {
    "items": [
      {
        "id": 5,
        "created_at": 1387348804000,
        "uid": "123",
        "user_id": 5,
        "is_friend": true
      },
      {
        "id": 6,
        "created_at": 1387348812000,
        "uid": "1234609293",
        "user_id": 6,
        "is_friend": null
      }
    ]
  },
  "status": "success"
}
```

## POST /api/greetings

对某人打招呼，如果返回 `is_friend` 为 `true` 则表示对方已经对这个人打过招呼了

### parameter:

* uid: string
* provider: string (目前只能是"weibo")

### return

```
{
  "status": "success",
  "data": {
    "is_friend": false,
    "user_id": 123
  }
}
```
