import numpy as np
from jamo import h2j, j2hcj  # 자모 분리 라이브러리
from difflib import SequenceMatcher

def cer(reference, hypothesis):
    """한글 CER을 계산하는 함수. 자모 단위로 문장을 비교합니다."""
    
    # 자모 단위로 변환하여 비교
    ref = j2hcj(h2j(reference))
    hyp = j2hcj(h2j(hypothesis))

    # Levenshtein Distance 계산
    matcher = SequenceMatcher(None, ref, hyp)
    edits = sum([sum(triple[-2:]) for triple in matcher.get_opcodes() if triple[0] != 'equal'])

    # CER 계산
    cer_score = edits / max(len(ref), 1)
    return cer_score

# 샘플 데이터 (참조 텍스트와 OCR 결과 텍스트)
reference_text = "안녕하세요"
hypothesis_text = "안뇽하세요"  # OCR 결과 예시

# CER 계산
cer_score = cer(reference_text, hypothesis_text)
print(f"CER: {cer_score:.4f}")
