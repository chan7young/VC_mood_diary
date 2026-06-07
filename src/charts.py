"""담당 ③: 대시보드용 데이터 가공."""
import pandas as pd


def emotions_over_time(entries):
    """일기별 대표 감정 강도를 시계열 DataFrame 으로 변환."""
    rows = []
    for e in entries:
        emos = e.get("analysis", {}).get("emotions", [])
        top = max(emos, key=lambda x: x.get("intensity", 0)) if emos else None
        rows.append({
            "date": e.get("date", ""),
            "감정": top["label"] if top else "기록 없음",
            "강도": top["intensity"] if top else 0,
        })
    return pd.DataFrame(rows)


def keyword_counts(entries):
    """전체 일기에서 키워드 빈도 집계."""
    counts = {}
    for e in entries:
        for kw in e.get("analysis", {}).get("keywords", []):
            counts[kw] = counts.get(kw, 0) + 1
    return pd.DataFrame(
        sorted(counts.items(), key=lambda x: -x[1]),
        columns=["키워드", "횟수"],
    )
