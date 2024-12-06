# import openai
# import pandas as pd
# import numpy as np
# from pydantic import BaseModel
#
#
#
# length_max = 0
#
# file = pd.read_csv("./data.csv")
# print(file.info)
# print(file.describe())
# print(file.keys())
# #
# for i in range(1, 232074):
#     text = file.loc[i, "text"]

import openai
import pandas as pd
import numpy as np
import time
from tqdm import tqdm


def translate_text(text, api_key, model="gpt-4o-mini"):
    """
    OpenAI API를 사용하여 텍스트를 한국어로 번역합니다.
    오류 발생 시 최대 3번 재시도합니다.
    """
    client = openai.OpenAI(api_key=api_key)
    max_retries = 3
    system_prompt = """
        당신은 영어를 한국어로 번역하는 전문 번역가입니다. 
        다음 지침을 따라 번역해주세요:
        1. 직역보다는 한국어 화자가 자연스럽게 이해할 수 있도록 의역하세요.
        2. 인터넷 커뮤니티나 SNS의 문체를 반영해주세요.
        3. 이모지나 특수문자는 한국 인터넷 문화에 맞게 적절히 변환하세요.
        4. 은어나 속어는 한국의 상응하는 표현으로 바꿔주세요.
        5. 문맥상 생략된 내용이 있다면 자연스럽게 보완해주세요.
        """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"{system_prompt}"},
                    {"role": "user", "content": f"Translate the following text to Korean: {text}"}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error translating text: {str(e)}")
                return "번역 실패"
            time.sleep(1)  # API 재시도 전 1초 대기


def process_dataframe(file_path, api_key, batch_size=100):

    # 원본 데이터 읽기
    df = pd.read_csv(file_path)
    df['korean_text'] = ''

    # 진행 상황을 표시하기 위한 tqdm 설정
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i + batch_size]

        for idx, row in batch.iterrows():
            korean_text = translate_text(row['text'], api_key)
            df.at[idx, 'korean_text'] = korean_text
            print(korean_text)
        if i % 1000 == 0:
            df.to_csv(f'translated_data_backup_{i}.csv', index=False, encoding="utf-8")
        time.sleep(0.5)

    # 최종 결과 저장
    df.to_csv('translated_data_final.csv', index=False, encoding="utf-8")
    return df


def main():
    
    API_KEY = ""

    # 데이터 처리 시작
    translated_df = process_dataframe("./data.csv", API_KEY)

    # 결과 확인
    print("\n번역 완료!")
    print(f"총 처리된 데이터 수: {len(translated_df)}")
    print("\n번역 샘플:")
    print(translated_df[['text', 'korean_text', 'class']].head())


if __name__ == "__main__":
    main()