Go to github for this [README](https://github.com/aisensiy/dianying/blob/master/README.md).

## APIS

* GET   /api/movies/(coming|playing)
* GET   /api/messages -- require login
* POST  /api/messages -- require login
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

## POST /auth/login

如果这个用户是第一次授权连接我们的应用，那么就会为他建立一个新的账号。否则就返回他的账号。其中 `uid` 是微博账号的 `id` 而 `user_id` 是我们为他创建的账号id。在其他地方使用到的 `user_id` 都是指这个账号。

### paramters:

* access_token: string

### return

```
{
    "uid": "1313608362",
    "user_id": 3
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

## GET /api/messages

### parameters:

* user_id: int
* limit: int
* offset: int

### return:

```
{
  "data": {
    "items": [
      {
        "content": "test",
        "created_at": "Fri, 29 Nov 2013 18:50:44 GMT",
        "id": 7
      },
      {
        "content": "test",
        "created_at": "Fri, 29 Nov 2013 18:50:46 GMT",
        "id": 8
      },
      {
        "content": "test",
        "created_at": "Sat, 30 Nov 2013 02:56:13 GMT",
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
    "content": "test",
    "created_at": "Sat, 30 Nov 2013 04:43:01 GMT",
    "dst_user_id": 1,
    "id": 14,
    "src_user_id": 1
  },
  "status": "success"
}
```

## GET /api/friends

返回相互打过招呼的好友列表

### parameters:

* limit: int
* offset: int

### return

```
{
  "data": {
    "items": [
      {
        "user_id": 5,
        "provider": "weibo",
        "uid": "123"
      },
      {
        "user_id": 3,
        "provider": "weibo",
        "uid": "1313608362"
      }
    ]
  },
  "status": "success"
}
```

## GET /api/greetings

提供微博 uid 的列表，返回哪些已经打过招呼了。

### parameters:

* weibo: 以逗号分隔的数组 例如 `/api/greetings?weibo=1,2,3`

### return

返回已经打过招呼的 uid 列表

```
{
  "data": {
    "items": {
      "weibo": [ "123", "456" ]
    }
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
  "is_friend": false,
  "status": "success"
}
```
