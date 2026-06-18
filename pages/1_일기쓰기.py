import streamlit as st
from src.storage import save_entry
from src.analysis import analyze_entry


st.title("📝 오늘의 일기")


diary = st.text_area(
    "오늘 하루는 어땠나요?",
    height=200
)


if st.button("저장하기"):

    if diary.strip():
        analysis = analyze_entry(diary)

        # 위기 신호가 감지되면 상담 자원을 안내하고 분석/저장은 하지 않는다.
        if analysis.get("crisis"):
            st.error(analysis.get("message", ""))
        else:
            save_entry(diary, analysis)
            st.success("일기가 저장되었습니다 🌙")

            # API 키가 없으면 고정된 예시(mock) 결과가 나오므로 안내
            if analysis.get("mock"):
                st.warning(
                    "⚠️ 현재 API 키가 없어 예시(mock) 분석 결과가 표시됩니다. "
                    "실제 감정 분석을 보려면 .env 파일에 GEMINI_API_KEY를 설정하세요."
                )

            # 분석 결과 표시
            emotions = analysis.get("emotions", [])
            if emotions:
                st.subheader("감정 분석")
                for emo in emotions:
                    st.write(f"• {emo.get('label')} (강도 {emo.get('intensity')}/5)")

            keywords = analysis.get("keywords", [])
            if keywords:
                st.subheader("주요 키워드")
                st.write(" · ".join(keywords))

            comment = analysis.get("comment")
            if comment:
                st.info(comment)

    else:
        st.warning("내용을 입력해주세요.")
