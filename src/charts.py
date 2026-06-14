"""담당 ③: 대시보드용 데이터 가공."""
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter


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


def weekly_summary(entries):
    """최근 7일 일기를 요약해 dict 로 반환한다.

    반환 형태:
        {
            "count": 기록 수 (int),
            "top_emotion": 가장 많이 등장한 감정 레이블 (str),
            "avg_intensity": 감정 강도 평균 (float, 소수 1자리),
        }

    동작 방식:
    1. 오늘 날짜를 기준으로 7일 전 날짜(cutoff)를 계산한다.
    2. entries 를 순회하며 date 필드가 cutoff 이후인 항목만 추린다.
    3. 추린 항목 각각의 emotions 리스트를 펼쳐 레이블과 강도를 수집한다.
    4. Counter 로 레이블 등장 횟수를 세어 가장 많은 것을 top_emotion 으로 삼는다.
    5. 모든 강도 값의 평균을 소수 1자리로 반올림해 avg_intensity 로 반환한다.
    """
    # ① 기준 날짜 계산: 오늘 자정 - 7일
    cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)

    # ② 최근 7일 항목만 걸러내기
    recent = []
    for e in entries:
        try:
            # date 문자열을 datetime 객체로 변환 (예: "2026-06-01 21:10")
            entry_dt = datetime.strptime(e.get("date", ""), "%Y-%m-%d %H:%M")
        except ValueError:
            continue  # 날짜 형식이 맞지 않으면 건너뜀
        if entry_dt >= cutoff:
            recent.append(e)

    # ③ 감정 레이블·강도를 모두 수집
    labels = []       # 감정 이름 목록 (같은 감정이 여러 번 나올 수 있음)
    intensities = []  # 강도 숫자 목록

    for e in recent:
        for emo in e.get("analysis", {}).get("emotions", []):
            label = emo.get("label")
            intensity = emo.get("intensity")
            if label:
                labels.append(label)
            if intensity is not None:
                intensities.append(intensity)

    # ④ 가장 많이 등장한 감정 찾기
    if labels:
        # Counter(labels) → {"피곤함": 3, "불안": 2, ...}
        # .most_common(1) → [("피곤함", 3)]
        top_emotion = Counter(labels).most_common(1)[0][0]
    else:
        top_emotion = None  # 기록이 없으면 None

    # ⑤ 평균 강도 계산
    if intensities:
        avg_intensity = round(sum(intensities) / len(intensities), 1)
    else:
        avg_intensity = None  # 기록이 없으면 None

    return {
        "count": len(recent),
        "top_emotion": top_emotion,
        "avg_intensity": avg_intensity,
    }
