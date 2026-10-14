import random

import streamlit as st

# ------------------------------------------------------------
# MBTI로 단짝 포켓몬 찾기 (Streamlit 앱 1개 파일)
# 실행: streamlit run main.py
# ------------------------------------------------------------

st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="⚡",
    layout="centered",
)

# 포켓몬 공식 일러스트 (PokeAPI 공개 저장소)
IMG_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/pokemon/other/official-artwork/{}.png"
)

TYPE_COLORS = {
    "노말": "#A8A77A", "불꽃": "#EE8130", "물": "#6390F0", "전기": "#F7D02C",
    "풀": "#7AC74C", "얼음": "#96D9D6", "격투": "#C22E28", "독": "#A33EA1",
    "땅": "#E2BF65", "비행": "#A98FF3", "에스퍼": "#F95587", "벌레": "#A6B91A",
    "바위": "#B6A136", "고스트": "#735797", "드래곤": "#6F35FC",
    "강철": "#B7B7CE", "페어리": "#D685AD",
}

# MBTI -> 포켓몬 정보
DATA = {
    "INTJ": {
        "ko": "뮤츠", "en": "Mewtwo", "no": 150, "types": ["에스퍼"],
        "trait": "강력한 초능력을 지닌 전설의 포켓몬. 냉철하고 고독해요.",
        "reasons": [
            "혼자 깊이 생각하고 큰 계획을 세우는 모습이 닮았어요.",
            "겉은 차분하지만 속에는 강한 신념과 실력을 숨기고 있어요.",
            "목표를 정하면 끝까지 해내는 전략가 같은 단짝이에요.",
        ],
    },
    "INTP": {
        "ko": "후딘", "en": "Alakazam", "no": 65, "types": ["에스퍼"],
        "trait": "IQ가 5000이라고 알려진 천재 포켓몬. 숟가락을 들고 있어요.",
        "reasons": [
            "궁금한 건 끝까지 파고드는 탐구자 스타일이에요.",
            "머릿속에서는 늘 새로운 생각이 돌아가고 있어요.",
            "말수는 적어도 필요할 땐 똑똑한 해답을 내놓는 단짝이에요.",
        ],
    },
    "ENTJ": {
        "ko": "리자몽", "en": "Charizard", "no": 6, "types": ["불꽃", "비행"],
        "trait": "하늘을 날며 뜨거운 불꽃을 내뿜는 당당한 포켓몬이에요.",
        "reasons": [
            "앞장서서 팀을 이끄는 당당한 리더 타입과 닮았어요.",
            "목표가 생기면 뜨겁게 불타오르는 열정이 있어요.",
            "자신감 있게 길을 열어 주는 믿음직한 단짝이에요.",
        ],
    },
    "ENTP": {
        "ko": "팬텀", "en": "Gengar", "no": 94, "types": ["고스트", "독"],
        "trait": "그림자 속에 숨어 장난치기를 좋아하는 장난꾸러기예요.",
        "reasons": [
            "장난기 넘치고 재치 있는 말솜씨가 꼭 닮았어요.",
            "틀에 박힌 건 싫어하고 새로운 도전을 즐겨요.",
            "토론하고 아이디어 내는 걸 좋아하는 분위기 메이커 단짝이에요.",
        ],
    },
    "INFJ": {
        "ko": "가디안", "en": "Gardevoir", "no": 282, "types": ["에스퍼", "페어리"],
        "trait": "소중한 사람을 지키기 위해 힘을 쓰는 다정한 수호자예요.",
        "reasons": [
            "다른 사람의 마음을 먼저 알아채는 따뜻한 수호자 같아요.",
            "조용하지만 소중한 사람을 위해선 용감해져요.",
            "깊은 공감과 직관으로 곁을 지켜 주는 단짝이에요.",
        ],
    },
    "INFP": {
        "ko": "이브이", "en": "Eevee", "no": 133, "types": ["노말"],
        "trait": "여러 모습으로 진화할 수 있는 가능성의 포켓몬이에요.",
        "reasons": [
            "무엇이든 될 수 있는 가능성을 품은 순수한 마음이 닮았어요.",
            "자기만의 감성과 가치관을 소중히 여겨요.",
            "여리지만 좋아하는 것 앞에선 누구보다 진심인 단짝이에요.",
        ],
    },
    "ENFJ": {
        "ko": "루카리오", "en": "Lucario", "no": 448, "types": ["격투", "강철"],
        "trait": "상대의 기운(파동)을 읽을 수 있는 의리 있는 포켓몬이에요.",
        "reasons": [
            "친구들을 이끌고 챙기는 의리파 리더와 닮았어요.",
            "다른 사람의 감정을 잘 읽고 힘이 되어 줘요.",
            "정의감과 따뜻함을 함께 가진 든든한 단짝이에요.",
        ],
    },
    "ENFP": {
        "ko": "피카츄", "en": "Pikachu", "no": 25, "types": ["전기"],
        "trait": "볼의 전기 주머니로 찌릿찌릿 전기를 모으는 인기 포켓몬이에요.",
        "reasons": [
            "어디서나 분위기를 밝게 만드는 에너지 덩어리예요.",
            "사람을 좋아하고 새로운 일에 신나게 뛰어들어요.",
            "누구와도 금방 친해지는 사랑스러운 매력의 단짝이에요.",
        ],
    },
    "ISTJ": {
        "ko": "거북왕", "en": "Blastoise", "no": 9, "types": ["물"],
        "trait": "등껍질의 강력한 물대포로 든든하게 지켜 주는 포켓몬이에요.",
        "reasons": [
            "맡은 일은 꼼꼼하게 끝까지 책임지는 성실함이 닮았어요.",
            "단단한 껍질처럼 흔들림 없이 원칙을 지켜요.",
            "말보다 행동으로 믿음을 주는 든든한 단짝이에요.",
        ],
    },
    "ISFJ": {
        "ko": "해피너스", "en": "Blissey", "no": 242, "types": ["노말"],
        "trait": "다친 이에게 행복의 알을 나눠 주는 상냥한 포켓몬이에요.",
        "reasons": [
            "주변 사람을 세심하게 챙기는 따뜻한 돌봄이 닮았어요.",
            "눈에 띄지 않아도 묵묵히 곁을 지켜 줘요.",
            "상대가 필요한 걸 먼저 알아채는 배려의 달인 단짝이에요.",
        ],
    },
    "ESTJ": {
        "ko": "윈디", "en": "Arcanine", "no": 59, "types": ["불꽃"],
        "trait": "엄청난 속도로 달리는 용맹하고 충직한 전설의 포켓몬이에요.",
        "reasons": [
            "규칙과 질서를 지키며 팀을 이끄는 리더 스타일이에요.",
            "듬직하고 의리 있어서 믿고 맡길 수 있어요.",
            "정해진 목표를 향해 힘차게 달려가는 실행가 단짝이에요.",
        ],
    },
    "ESFJ": {
        "ko": "라프라스", "en": "Lapras", "no": 131, "types": ["물", "얼음"],
        "trait": "사람을 등에 태우고 바다를 건너 주는 상냥한 포켓몬이에요.",
        "reasons": [
            "사람들을 등에 태우고 함께 가는 다정한 친구 같아요.",
            "모두가 편안하도록 분위기를 챙겨 줘요.",
            "베푸는 걸 좋아하고 모임에서 인기 많은 단짝이에요.",
        ],
    },
    "ISTP": {
        "ko": "나옹", "en": "Meowth", "no": 52, "types": ["노말"],
        "trait": "반짝이는 걸 좋아하고 눈치 빠르게 돌아다니는 고양이 포켓몬이에요.",
        "reasons": [
            "평소엔 느긋하다가 필요할 땐 재빠른 자유로운 영혼이에요.",
            "말은 적지만 문제 해결 능력이 좋아요.",
            "간섭받는 건 싫어하고 내 방식대로 움직이는 쿨한 단짝이에요.",
        ],
    },
    "ISFP": {
        "ko": "치코리타", "en": "Chikorita", "no": 152, "types": ["풀"],
        "trait": "머리의 잎에서 나는 은은한 향기로 마음을 편안하게 해 줘요.",
        "reasons": [
            "조용하고 온화해서 곁에 있으면 마음이 편해져요.",
            "자연과 예쁜 것을 좋아하는 감성파예요.",
            "다투기보다 자기만의 속도로 살아가는 순한 단짝이에요.",
        ],
    },
    "ESTP": {
        "ko": "한카리아스", "en": "Garchomp", "no": 445, "types": ["드래곤", "땅"],
        "trait": "제트기처럼 빠르게 날아다니는 사냥꾼 같은 포켓몬이에요.",
        "reasons": [
            "생각보다 행동이 먼저 나가는 시원시원한 모험가예요.",
            "빠른 판단력으로 위기에도 당황하지 않아요.",
            "스릴과 도전을 즐기는 액션 스타 단짝이에요.",
        ],
    },
    "ESFP": {
        "ko": "푸린", "en": "Jigglypuff", "no": 39, "types": ["노말", "페어리"],
        "trait": "노래로 모두를 잠재우는, 무대를 사랑하는 포켓몬이에요.",
        "reasons": [
            "노래하고 춤추며 모두를 즐겁게 하는 분위기 스타예요.",
            "지금 이 순간을 마음껏 즐길 줄 알아요.",
            "표정과 감정이 솔직해서 사랑받는 매력의 단짝이에요.",
        ],
    },
}

ORDER = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

# ------------------------------------------------------------
# 스타일 (크림 · 노란색 톤, 큰 글씨)
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background: #FFF8E1; }
    html, body, [class*="css"], .stMarkdown, p, li, span {
        font-size: 20px;
        color: #5D4037;
    }
    .block-container { max-width: 760px; padding-top: 2rem; }

    .main-title {
        text-align: center; font-size: 2.3rem; font-weight: 800;
        color: #5D4037; margin: 0 0 6px 0; line-height: 1.3;
    }
    .sub-title {
        text-align: center; font-size: 1.15rem; color: #8D6E63; margin-bottom: 22px;
    }

    /* MBTI 버튼 */
    div.stButton > button {
        width: 100%;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        padding: 0.9rem 0.2rem;
        border-radius: 18px;
        border: 3px solid #FFCA28;
        background: #FFFFFF;
        color: #5D4037;
        box-shadow: 0 4px 0 #F9A825;
    }
    div.stButton > button:hover {
        background: #FFE082; border-color: #FFCA28; color: #5D4037;
    }
    div.stButton > button[kind="primary"] {
        background: #FFCA28; border-color: #F9A825; color: #5D4037;
    }
    div.stButton > button p { font-size: 1.3rem !important; font-weight: 800 !important; }

    /* 결과 카드 */
    .banner {
        text-align: center; background: #FFECB3; border-radius: 999px;
        padding: 10px 18px; font-weight: 800; font-size: 1.3rem;
        margin: 22px 0 14px 0; color: #5D4037;
    }
    .poke-card {
        background: #FFFFFF; border: 4px solid #FFCA28; border-radius: 28px;
        padding: 18px 22px 24px 22px; box-shadow: 0 8px 0 #F9A825;
        text-align: center;
    }
    .poke-name { font-size: 2.2rem; font-weight: 800; margin: 6px 0 0 0; }
    .poke-en { font-size: 1.2rem; color: #8D6E63; margin: 0 0 12px 0; }
    .chip {
        display: inline-block; color: #FFFFFF; font-weight: 800;
        border-radius: 999px; padding: 4px 18px; margin: 0 4px; font-size: 1.1rem;
        text-shadow: 0 1px 2px rgba(0,0,0,.35);
    }
    .trait {
        background: #FFF8E1; border-radius: 16px; padding: 12px 16px;
        margin: 16px 0 12px 0; font-size: 1.15rem;
    }
    .reason {
        background: #FFF8E1; border-radius: 16px; padding: 14px 18px;
        text-align: left; font-size: 1.15rem;
    }
    .reason p { margin: 0 0 6px 0; font-size: 1.15rem; }
    .reason p:last-child { margin-bottom: 0; }
    .mini-title { font-weight: 800; font-size: 1.2rem; margin: 14px 0 6px 0; text-align: left; }

    /* 축하 꽃가루 효과 (CSS만 사용) */
    .confetti {
        position: fixed; top: -60px; z-index: 9999; pointer-events: none;
        animation-name: fall; animation-timing-function: linear;
        animation-fill-mode: forwards; animation-iteration-count: 1;
    }
    @keyframes fall {
        0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
        85%  { opacity: 1; }
        100% { transform: translateY(115vh) rotate(540deg); opacity: 0; }
    }

    @media (max-width: 600px) {
        html, body, [class*="css"], .stMarkdown, p, li, span { font-size: 18px; }
        .main-title { font-size: 1.75rem; }
        .poke-name { font-size: 1.8rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 상태 관리
# ------------------------------------------------------------
if "mbti" not in st.session_state:
    st.session_state.mbti = None
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False


def choose(code: str) -> None:
    st.session_state.mbti = code
    st.session_state.celebrate = True


def reset() -> None:
    st.session_state.mbti = None
    st.session_state.celebrate = False


def confetti_html(count: int = 40) -> str:
    """하늘에서 떨어지는 이모지 꽃가루."""
    pieces = ["🎉", "✨", "⭐", "💛", "🎊", "⚡"]
    rnd = random.Random()
    spans = []
    for _ in range(count):
        left = rnd.randint(0, 98)
        size = rnd.randint(22, 42)
        delay = rnd.random() * 1.5
        duration = 2.8 + rnd.random() * 2.5
        icon = rnd.choice(pieces)
        spans.append(
            f'<span class="confetti" style="left:{left}vw;font-size:{size}px;'
            f'animation-delay:{delay:.2f}s;animation-duration:{duration:.2f}s;">{icon}</span>'
        )
    return "".join(spans)


# ------------------------------------------------------------
# 화면
# ------------------------------------------------------------
st.markdown('<div class="main-title">⚡ MBTI로 단짝 포켓몬 찾기</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">내 MBTI 유형을 눌러 보세요. 나와 닮은 단짝 포켓몬을 찾아 드려요!</div>',
    unsafe_allow_html=True,
)

# 16개 유형 버튼 (4 x 4)
for row_start in range(0, 16, 4):
    cols = st.columns(4)
    for col, code in zip(cols, ORDER[row_start:row_start + 4]):
        with col:
            st.button(
                code,
                key=f"btn_{code}",
                on_click=choose,
                args=(code,),
                type="primary" if st.session_state.mbti == code else "secondary",
                use_container_width=True,
            )

# 결과
code = st.session_state.mbti
if code:
    p = DATA[code]

    # 축하 효과
    if st.session_state.celebrate:
        st.balloons()
        st.markdown(confetti_html(), unsafe_allow_html=True)
        st.session_state.celebrate = False

    st.markdown(
        f'<div class="banner">🎉 축하해요! {code}의 단짝 포켓몬을 찾았어요! 🎉</div>',
        unsafe_allow_html=True,
    )

    type_chips = "".join(
        f'<span class="chip" style="background:{TYPE_COLORS.get(t, "#999")}">{t}</span>'
        for t in p["types"]
    )
    reasons_html = "".join(f"<p>✔ {line}</p>" for line in p["reasons"])
    img_src = IMG_URL.format(p["no"])

    st.markdown(
        f"""
        <div class="poke-card">
            <img src="{img_src}" alt="{p['ko']} ({p['en']})"
                 style="width:min(300px, 70%); height:auto;" />
            <div class="poke-name">{p['ko']}</div>
            <div class="poke-en">{p['en']} · 도감번호 {p['no']}</div>
            <div>{type_chips}</div>
            <div class="trait">📖 <b>특징</b><br>{p['trait']}</div>
            <div class="mini-title">💛 {code}와 어울리는 이유</div>
            <div class="reason">{reasons_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.button("🔄 다시 고르기", on_click=reset, use_container_width=True)

st.write("")
st.caption("포켓몬 이미지는 PokeAPI 공개 저장소에서 불러옵니다. 포켓몬은 ⓒ Nintendo / Creatures / GAME FREAK 의 저작물이에요.")
