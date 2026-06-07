"""담당 ②: LLM 감정·키워드 분석 + 위기 안전장치.

설계 원칙
- 진단하지 않는다. 우울증 점수 같은 의학적 판정 금지. '관찰'만 한다.
- 위기 신호가 보이면 분석 대신 상담 자원 안내를 우선한다.
- API 키가 없으면 mock 모드로 동작해, 키 없이도 앱 시연이 가능하다.
"""
import os
import json
import re

# ── 위기 신호 키워드(예시). 실제 운영 전 신중히 보완하세요. ──────────────
CRISIS_KEYWORDS = ["죽고 싶", "자살", "사라지고 싶", "살기 싫", "자해"]

# ⚠️ 구현 시 공식 최신 상담 번호로 반드시 확인 후 교체하세요.
CRISIS_RESOURCE_TEXT = (
    "지금 많이 힘드신 것 같아요. 혼자 견디지 않으셔도 됩니다.\n\n"
    "전문 상담 자원에 연결되실 수 있어요. "
    "(여기에 본인 지역의 공식 위기상담 연락처를 확인해 기입하세요.)"
)


def detect_crisis(text: str) -> bool:
    """일기에 위기 신호가 있는지 단순 키워드로 1차 판별."""
    return any(kw in text for kw in CRISIS_KEYWORDS)


def _mock_analysis(text: str) -> dict:
    """API 키가 없을 때 쓰는 가짜 분석 결과(시연·개발용)."""
    return {
        "emotions": [{"label": "차분함", "intensity": 3}, {"label": "약간의 불안", "intensity": 2}],
        "keywords": ["하루", "생각"],
        "comment": "오늘 하루를 돌아본 점이 좋아요. (※ mock 모드: 실제 분석이 아닙니다)",
    }


def analyze_entry(text: str) -> dict:
    """일기 한 편을 분석해 감정/키워드/코멘트를 반환한다."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("여기에"):
        return _mock_analysis(text)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        prompt = (
            "너는 일기 분석 보조 도구다. 의학적 진단이나 점수를 매기지 말고, "
            "관찰한 감정과 반복 주제만 알려줘. 아래 일기를 읽고 JSON만 출력해.\n"
            '형식: {"emotions":[{"label":"감정","intensity":1~5}], '
            '"keywords":["주제"], "comment":"따뜻한 성찰 한마디"}\n\n'
            f"일기:\n{text}"
        )
        resp = model.generate_content(prompt)
        raw = re.sub(r"```json|```", "", resp.text).strip()
        return json.loads(raw)
    except Exception:
        # 호출 실패 시에도 앱이 멈추지 않게 mock 으로 안전 복귀
        return _mock_analysis(text)
