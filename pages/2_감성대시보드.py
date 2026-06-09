"""담당 ③: 감정 추이·키워드 대시보드."""
import streamlit as st
from src.storage import load_entries
from src.charts import emotions_over_time, keyword_counts, weekly_summary  # ← weekly_summary 추가

st.title("📊 감정 대시보드")

entries = load_entries()
if not entries:
    st.info("아직 일기가 없어요. 먼저 '일기쓰기'에서 기록을 남겨주세요.")
else:
    # ⬇️ 여기부터 새로 추가한 요약 카드
    summary = weekly_summary(entries)
    st.subheader("이번 주 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("기록 수", f"{summary['count']}개")
    col2.metric("가장 많은 감정", summary["top_emotion"])
    col3.metric("평균 감정 강도", f"{summary['avg_intensity']} / 5")
    # ⬆️ 여기까지 추가

    st.subheader("감정 강도 추이")
    df = emotions_over_time(entries)
    st.line_chart(df, x="date", y="강도")

    st.subheader("자주 등장한 주제")
    kw = keyword_counts(entries)
    if not kw.empty:
        st.bar_chart(kw, x="키워드", y="횟수")

    st.subheader("최근 기록")
    for e in reversed(entries[-5:]):
        with st.expander(e["date"]):
            st.write(e["text"])