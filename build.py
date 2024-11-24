from tqdm import tqdm
from json import dumps
from csv import DictReader

from math import ceil

prompt = ""
max_tokens = 1000
limit = 30000
max_csv = 232074

with open("data.csv", newline='') as c:
  r = DictReader(c)
  for i in range(ceil(max_csv / limit)):
    with open(f"input_{i}.jsonl", "w") as f:
      count = i*limit
      inner_count = 0
      for j in tqdm(r):
        inner_count += 1
        if inner_count > limit or count+inner_count > max_csv:
          break
        suicidial = j["class"] == "suicide"
        value = j["text"]
        f.write(f"{dumps({
          "custom_id": f"request-{inner_count}",
          "method": "POST",
          "url": "/v1/chat/completions",
          "body": {
            "model": "gpt-4o",
            "messages": [
              {"role": "system", "content": prompt},
              {"role": "user", "content": f'text: {value}'}
            ],
            "max_tokens": max_tokens
          }
        })}\n")

print("finsihed")
