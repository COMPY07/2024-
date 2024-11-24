from tqdm import tqdm
from tiktoken import get_encoding

from json import dumps
from csv import DictReader
from pathlib import Path

enc = get_encoding("o200k_base") # gpt4o - https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
# test
assert enc.decode(enc.encode("hello world")) == "hello world"
prompt = ""
prompt_encode = len(enc.encode(prompt))
max_tokens = 1000
max_tokens_batch = 90000
limit = 50000
count = 0
token_count = 0
base_path = Path("./inputs")
if not base_path.is_dir():
  base_path.mkdir()

with open("data.csv", newline='') as c:
  r = list(DictReader(c))
  max_csv = len(r)
  print(max_csv)
  i = 0
  while count < max_csv:
    with open(base_path.joinpath(f"{i}.jsonl"), "w") as f:
      inner_count = 0
      token_count = 0
      for j in tqdm(r[count:]):
        next_token_count = token_count+prompt_encode+len(enc.encode(r[count+1]['text']))
        if inner_count >= limit or count >= max_csv or next_token_count >= max_tokens_batch:
          print('early break')
          print(f'inner_count >= limit: {inner_count >= limit}')
          print(f'count >= max_csv: {count >= max_csv}')
          print(next_token_count, max_tokens_batch)
          if next_token_count >= max_tokens_batch and inner_count == 0:
            print(f"{count+1} has a lot of data that exceeds max token alone")
            exit(1)
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
        inner_count += 1
        count += 1
        token_count += len(enc.encode(f'text: {value}')) + prompt_encode
    i += 1

print("finsihed")
