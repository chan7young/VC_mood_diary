"""무드 다이어리 메인 진입점"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------
# 페이지 설정
# --------------------
st.set_page_config(
    page_title="Mood Diary",
    page_icon="🌙",
    layout="centered",
)

# --------------------
# 커스텀 스타일
# --------------------
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            color: #7C5CFC;
            margin-bottom: 0.5rem;
        }

        .sub-title {
            text-align: center;
            color: #6B7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        .feature-box {
            padding: 1rem;
            border-radius: 12px;
            background-color: rgba(124,92,252,0.08);
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------
# 홈 화면
# --------------------
st.markdown(
    '<div class="main-title">🌙 Mood Diary</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sub-title">
    오늘의 감정을 기록하고,<br>
    나만의 감정 패턴을 발견해 보세요.
    </div>
    """,
    unsafe_allow_html=True,
)

# 안내 문구
st.info(
    """
    이 서비스는 사용자의 감정을 기록하고 성찰할 수 있도록 돕는 도구입니다.

    • 감정 일기 작성  
    • AI 기반 감정 분석  
    • 감정 변화 추적 및 시각화  

    ※ 본 서비스는 의료적 진단이나 심리 상담을 대체하지 않습니다.
    """,
    icon="💜",
)

st.divider()

# 주요 기능 소개
st.subheader("✨ 주요 기능")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="feature-box">
        <h4>📝 감정 일기 작성</h4>
        하루 동안 느낀 감정을 자유롭게 기록합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-box">
        <h4>🤖 AI 감정 분석</h4>
        작성한 일기에서 주요 감정과 키워드를 분석합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-box">
        <h4>📊 감정 대시보드</h4>
        감정의 흐름과 패턴을 한눈에 확인합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-box">
        <h4>🌱 자기 성찰</h4>
        감정 기록을 통해 자신을 더 깊이 이해합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# 사용 방법
st.subheader("📌 사용 방법")

st.markdown(
    """
    1. 사이드바에서 **일기쓰기** 메뉴 선택
    2. 오늘의 감정을 작성
    3. AI 감정 분석 결과 확인
    4. **감정 대시보드**에서 변화 추이 확인
    """
)

st.success("오늘의 감정을 기록하며 스스로를 이해하는 시간을 가져보세요 🌙")

# 사이드바
with st.sidebar:
    st.title("🌙 Mood Diary")

    st.markdown(
        """
        ### 메뉴 안내

        ✍️ 일기쓰기

        📊 감정대시보드

        ⚙️ 설정
        """
    )

    st.divider()

    st.caption("Version 1.0")