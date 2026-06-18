# src/analysis.py

import os
import json
import google.generativeai as genai

# ----------------------------
# 위기 키워드
# ----------------------------
CRISIS_KEYWORDS = [
    "죽고 싶",
    "살기 싫",
    "자살",
    "자해",
    "사라지고 싶"
]

# 위기 상황 안내 문구
CRISIS_RESOURCE_TEXT = """
힘든 시간을 보내고 계신 것 같습니다.

혼자 감당하지 않아도 괜찮습니다.

☎ 자살예방상담전화 : 109
☎ 정신건강상담전화 : 1577-0199
"""


# ----------------------------
# 위기 감지 함수
# ----------------------------
def detect_crisis(text: str) -> bool:
    text = text.lower()

    for keyword in CRISIS_KEYWORDS:
        if keyword in text:
            return True

    return False


# ----------------------------
# API가 없을 때 사용할 Mock 분석
# ----------------------------
def _mock_analysis(text: str):
    return {
        "crisis": False,
        "emotions": [
            {
                "label": "차분함",
                "intensity": 3
            },
            {
                "label": "약간의 불안",
                "intensity": 2
            }
        ],
        "keywords": [
            "하루",
            "생각"
        ],
        "comment": "오늘 하루를 돌아본 점이 인상적이네요."
    }


# ----------------------------
# 메인 분석 함수
# ----------------------------
def analyze_entry(text: str):

    # 1. 위기 상황 확인
    if detect_crisis(text):
        return {
            "crisis": True,
            "message": CRISIS_RESOURCE_TEXT
        }

    api_key = os.getenv("GEMINI_API_KEY")

    # API 키가 없으면 Mock 데이터 반환
    if not api_key:
        return _mock_analysis(text)

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite"
        )

        prompt = f"""
다음 일기를 분석하세요.

일기:
{text}

반드시 JSON 형식으로만 답하세요.

{{
  "emotions":[
    {{
      "label":"감정",
      "intensity":1
    }}
  ],
  "keywords":[
    "키워드1",
    "키워드2"
  ],
  "comment":"따뜻한 한마디"
}}
"""

        response = model.generate_content(prompt)

        result = json.loads(response.text)

        result["crisis"] = False

        return result

    except Exception as e:
        print("분석 오류:", e)

        return _mock_analysis(text)git