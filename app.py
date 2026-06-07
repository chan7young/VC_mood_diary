"""담당 ④(통합)/①(홈): 무드 다이어리 메인 진입점."""
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # .env 에서 GEMINI_API_KEY 불러오기

st.set_page_config(page_title="무드 다이어리", page_icon="🌙", layout="centered")

st.title("🌙 무드 다이어리")
st.write("하루의 감정을 적으면, 패턴을 함께 살펴봐 드려요.")

st.info(
    "이 앱은 **자기 이해를 돕는 성찰 도구**이며, 의학적 진단이나 전문 상담을 "
    "대체하지 않습니다.",
    icon="💜",
)

st.markdown(
    "왼쪽 사이드바에서 **일기쓰기** → **감정대시보드** 순서로 사용해 보세요."
)
