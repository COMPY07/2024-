from httpx import get

from csv import DictWriter
from datetime import datetime, timedelta
from logging import basicConfig, ERROR, error
from traceback import format_exc
from copy import deepcopy

basicConfig(level=ERROR)

base_hashtag = "lang:ko -더바몰"
query = base_hashtag + " 자살"
print(query)
base_url = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"

# 2023/10~2024/10
now = datetime(2024, 10, 1, 0, 0)
since = deepcopy(now)
since -= timedelta(days=1)
since = since.replace(hour=0, minute=0, second=0, microsecond=0)
print(since)

with open("suicidal.csv", "w") as f:
  d = DictWriter(f, fieldnames=["id", "content"])
  d.writeheader()
  i = 0
  while i <= 12 * 31:
    try:
      params = {
        "q": query,
        "lang": "ko",
        "limit": 100,
        "sort": "top",
        "since": since.isoformat()[:19] + 'Z',
        "until": since.replace(
          day=since.day,
          hour=23,
          minute=59,
          second=59,
          microsecond=0
        ).isoformat()[:19] + 'Z'
      }
      print(params)
      data = get(base_url, params=params)
      print(data.status_code)
      if data.is_error:
        print(data.text)
        raise ValueError("it's error")
      print(data.json())
      print(data.headers)
      data = data.json()['posts']
      d.writerows([{'id': i['cid'], 'content': i['record']['text']} for i in data])
      since -= timedelta(days=1)
      i += 1
    except Exception as e:
      error(f"Error occurred: {e}\n{format_exc()}")
      input()

since = deepcopy(now)
since -= timedelta(days=1)
since = since.replace(hour=0, minute=0, second=0, microsecond=0)
print(since)

with open("normal.csv", "w") as f:
  d = DictWriter(f, fieldnames=["id", "content"])
  d.writeheader()
  i = 0
  while i <= 12 * 31:
    try:
      params = {
        "q": base_hashtag,
        "lang": "ko",
        "limit": 100,
        "sort": "top",
        "since": since.isoformat()[:19] + 'Z',
        "until": since.replace(
          day=since.day,
          hour=23,
          minute=59,
          second=59,
          microsecond=0
        ).isoformat()[:19] + 'Z'
      }
      print(params)
      data = get(base_url, params=params)
      print(data.status_code)
      if data.is_error:
        print(data.text)
        raise ValueError("it's error")
      print(data.json())
      print(data.headers)
      data = data.json()['posts']
      d.writerows([{'id': i['cid'], 'content': i['record']['text']} for i in data])
      since -= timedelta(days=1)
      i += 1
    except Exception as e:
      error(f"Error occurred: {e}\n{format_exc()}")
      input()
