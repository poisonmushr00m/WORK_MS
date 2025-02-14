import os
import re
import string
import jiwer

def custom_transform(text):
    # 만약 이미 리스트라면, 하나의 문자열로 결합
    if isinstance(text, list):
        text = ' '.join(text)
    # 대괄호 안의 내용(타임스탬프 등) 제거
    text = re.sub(r'\[[^\]]+\]', '', text)
    # 개행문자들을 공백으로 변경 및 다중 공백 통일
    text = re.sub(r'[\r\n]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    # 소문자화 (영어 알파벳에 영향)
    text = text.lower()
    # string.punctuation에 포함된 구두점 제거
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 토큰 단위로 split (각 토큰은 단어여야 함)
    tokens = text.split()
    if not tokens:
        tokens = ["<EMPTY>"]
    return tokens

# 1. Ground truth 파일 읽기
ground_truth_file = "duseoQkwlsfhaostm_lines_truth.txt"
with open(ground_truth_file, "r", encoding="utf-8") as f:
    ground_truth_text = f.read()

# 여러 줄이면 하나의 문자열로 결합 (공백으로 분리)
ground_truth_text = re.sub(r'[\r\n]+', ' ', ground_truth_text).strip()

print("Ground Truth Tokens:", custom_transform(ground_truth_text))

# 2. 결과 폴더 내의 모든 전사 파일에 대해 WER 계산
results_root = "result"  # 결과 폴더 최상위 디렉토리

for root, dirs, files in os.walk(results_root):
    for file in files:
        if file.endswith("_text.txt"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    hypothesis_text = f.read()
                
                # 디버그: 원본 텍스트 일부 및 전처리 결과 확인
                print(f"파일: {file_path}")
                print("원본 일부:", hypothesis_text[:100])
                print("전처리 후 토큰:", custom_transform(hypothesis_text))
                
                # jiwer를 이용해 WER 계산 (WER 결과는 0.1234 형태이면 12.34%로 출력)
                error = jiwer.wer(
                    ground_truth_text,
                    hypothesis_text,
                    truth_transform=custom_transform,
                    hypothesis_transform=custom_transform
                )
                print(f"WER: {error*100:.2f}%\n")
            except Exception as e:
                print(f"오류 발생 파일: {file_path}")
                print(e)