# APIS

* GET   /api/movies/(coming|playing)
* GET   /api/messages
* POST  /api/messages
* GET   /api/friends
* POST  /api/friends
* POST  /auth/login

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
        "aka": [
          "\u5f15\u529b\u8fb9\u7f18(\u6e2f)",
          "\u5730\u7403\u5f15\u529b",
          "\u91cd\u529b",
          "Gravedad"
        ],
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
          },
          {
            "alt": "http://movie.douban.com/celebrity/1048024/",
            "avatars": {
              "large": "http://img5.douban.com/img/celebrity/large/277.jpg",
              "medium": "http://img5.douban.com/img/celebrity/medium/277.jpg",
              "small": "http://img5.douban.com/img/celebrity/small/277.jpg"
            },
            "id": "1048024",
            "name": "\u827e\u5fb7\u00b7\u54c8\u91cc\u65af"
          },
          {
            "alt": "http://movie.douban.com/celebrity/1335305/",
            "avatars": {
              "large": "http://img3.douban.com/pics/celebrity-default-large.gif",
              "medium": "http://img3.douban.com/pics/celebrity-default-medium.gif",
              "small": "http://img3.douban.com/pics/celebrity-default-small.gif"
            },
            "id": "1335305",
            "name": "\u5965\u6258\u00b7\u4f0a\u683c\u5185\u4fee\u68ee"
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
