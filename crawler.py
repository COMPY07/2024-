from pydantic import BaseModel
from httpx import post, get
from openai import OpenAI

from time import sleep
from os import environ
from pathlib import Path

# https://scienceon.kisti.re.kr/srch/selectPORSrchArticle.do?cn=DIKO0015955197
hashtag = "자살 자살시도 자살충동 자살사고 죽고싶다 죽고싶어"
hashtags = [f"#{i}" for i in hashtag.split(" ")]
query = {
  "includeSearchTerms": False,
  "onlyImage": False,
  "onlyQuote": False,
  "onlyTwitterBlue": False,
  "onlyVerifiedUsers": False,
  "onlyVideo": False,
  "searchTerms": hashtags,
  "sort": "Latest",
  "tweetLanguage": "ko"
}

data_number = 10000 # data sum
if data_number % 2 == 1:
  raise ValueError("data_number must be even")
data_seq = data_number // 2
apify_id = "apidojo~tweet-scraper"
params = {"token": environ["APIFY_API_URL"]}

class GetRunResult(BaseModel):
  status: str

class RunActorResult(BaseModel):
  defaultDatasetId: str
  id: str

ids = {}

for _ in range(2):
  p = RunActorResult.model_validate_json(post(f"https://api.apify.com/v2/acts/{apify_id}/runs", params=params).json())
  ids[p.id] = p

data = []

while len(ids) > 0:
  res = []
  for i in ids:
    r = GetRunResult.model_validate_json(get(f"https://api.apify.com/v2/actor-runs/{i}").json())
    if r.status != "RUNNING":
      print(r.status)
      res.append(i)

  for i in res:
    print(i)
    data.extend(get(f"https://api.apify.com/v2/datasets/{ids[i].defaultDatasetId}/items").json())
    del ids[i]

  sleep(1)

Path("res.csv").write_text(data)
