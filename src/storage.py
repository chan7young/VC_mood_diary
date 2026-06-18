"""담당 ①: 일기 저장/불러오기 (간단한 로컬 JSON 저장)."""
import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "entries.json")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_entries.json")


def load_entries():
    """저장된 일기 목록을 불러온다.

    아직 저장된 일기가 없으면 샘플 데이터를 보여주고, 그것도 없으면 빈 리스트.
    """
    path = DATA_PATH if os.path.exists(DATA_PATH) else SAMPLE_PATH
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_entry(text, analysis):
    """일기 한 편과 분석 결과를 저장한다."""
    entries = load_entries()
    entries.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "text": text,
        "analysis": analysis,
    })
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    return entries
