import streamlit as st
from src.storage import save_entry


st.title("📝 오늘의 일기")


diary = st.text_area(
    "오늘 하루는 어땠나요?",
    height=200
)


if st.button("저장하기"):

    if diary.strip():
    save_entry(
        diary,
        {
            "emotions": [],
            "keywords": []
        }
    )

    st.success("일기가 저장되었습니다 🌙")

    else:
        st.warning("내용을 입력해주세요.")