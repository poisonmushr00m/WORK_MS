import re

def custom_transform(text):
    if isinstance(text, list):
        return text
    # 대괄호 안의 모든 내용 제거 (타임스탬프 등)
    text = re.sub(r'\[[^\]]+\]', '', text)
    # 개행 문자들을 공백으로 변경
    text = re.sub(r'[\r\n]+', ' ', text)
    # 다중 공백을 단일 공백으로 통일
    text = re.sub(r'\s+', ' ', text)
    # 소문자화
    text = text.lower()
    # 구두점 제거
    text = re.sub(r'[!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]', '', text)
    # 앞뒤 공백 제거 및 단어별 split
    tokens = text.strip().split()
    if not tokens:
        tokens = ["<EMPTY>"]
    return tokens


sample = "[00:00:00 - 00:00:01]   뭐야, 나 진짜 못했겠는데"
print(custom_transform(sample))
