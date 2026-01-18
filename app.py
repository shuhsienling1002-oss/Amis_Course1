import streamlit as st
import random
import time

# --- 0. 系統配置與 CSS 優化 (Layer 0: Pre-processing) ---
st.set_page_config(page_title="阿美語小教室", page_icon="🌞", layout="centered")

# 注入自定義 CSS 以適應低年級學童 (大字體、圓角、鮮豔色彩)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-size: 24px;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: scale(1.02);
    }
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
    }
    .med-font {
        font-size: 24px !important;
        color: #555;
        text-align: center;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 物理邏輯內核 (Layer 1: Data Structure) ---
# 依據您的修正更新詞彙庫
VOCABULARY = {
    "Fongoh": {"zh": "頭", "emoji": "🙆‍♂️", "action": "摸摸頭"},
    "Mata":   {"zh": "眼睛", "emoji": "👀", "action": "眨眨眼"},
    "Ngoso'": {"zh": "鼻子", "emoji": "👃", "action": "指鼻子"},
    "Tangila": {"zh": "耳朵", "emoji": "👂", "action": "拉耳朵"},
    "Ngoyos": {"zh": "嘴巴", "emoji": "👄", "action": "張開嘴"},  # User Corrected
    "Pising": {"zh": "臉頰/臉", "emoji": "😊", "action": "戳臉頰"} # User Corrected
}

SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？"},
    {"amis": "O {word} koni.", "zh": "這是{word}。"},
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。"},
    {"amis": "Tiyalen ko pising.", "zh": "摸摸臉頰。"}
]

# --- 2. 狀態管理 (Session State) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False

# --- 3. 介面邏輯 (UI Logic) ---

def show_learning_mode():
    st.markdown("<h1 style='text-align: center;'>🌞 阿美語身體歌 🌞</h1>", unsafe_allow_html=True)
    st.info("小朋友，跟著畫面一起唸唸看，做動作喔！")
    
    # 使用 2x3 網格展示單詞 (拓撲排列)
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        with (col1 if idx % 2 == 0 else col2):
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <div style="font-size: 60px;">{data['emoji']}</div>
                    <div class="big-font">{amis}</div>
                    <div class="med-font">{data['zh']}</div>
                    <div style="color: #888; font-size: 16px;">動作：{data['action']}</div>
                </div>
                """, unsafe_allow_html=True)
                # 模擬發音按鈕 (Streamlit 限制，這裡用文字反饋代替)
                if st.button(f"🔊 聽 {amis}", key=f"btn_{amis}"):
                    st.toast(f"正在播放：{amis} ({data['zh']})", icon="🔊")

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    st.success(f"Q: {SENTENCES[0]['amis']} ({SENTENCES[0]['zh']})")
    st.warning(f"A: {SENTENCES[1]['amis'].format(word='Mata')} (這是眼睛。)")

def show_quiz_mode():
    st.markdown("<h1 style='text-align: center;'>🎮 小勇士挑戰 🎮</h1>", unsafe_allow_html=True)
    
    # 進度條
    progress = st.progress(st.session_state.current_q / 3)
    
    # 題目邏輯 (Layer 2: Parallel Runtime)
    if st.session_state.current_q == 0:
        # 題目 1: 聽音辨位 (單詞 -> 圖片)
        st.markdown("### 第一關：聽聽看，這是誰？")
        st.markdown("<div class='big-font'>Tangila</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👃 鼻子"):
                st.error("不對喔，那是 Ngoso'！")
        with c2:
            if st.button("👂 耳朵"):
                st.balloons()
                st.success("答對了！Tangila 是耳朵！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("👀 眼睛"):
                st.error("不對喔，那是 Mata！")

    elif st.session_state.current_q == 1:
        # 題目 2: 句型重組 (邏輯)
        st.markdown("### 第二關：他問「O maan koni?」(這是什麼？)")
        st.markdown("#### 請幫忙回答： O _______ koni.")
        st.image("https://twemoji.maxcdn.com/v/latest/72x72/1f444.png", width=100) # 嘴巴圖示
        
        options = ["Fongoh (頭)", "Ngoyos (嘴巴)", "Pising (臉)"]
        choice = st.radio("請選擇正確的單詞：", options)
        
        if st.button("確定送出"):
            if "Ngoyos" in choice:
                st.success("太棒了！ O Ngoyos koni.")
                time.sleep(1)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再看仔細一點喔！圖片是嘴巴。")

    elif st.session_state.current_q == 2:
        # 題目 3: 動作指令 (TPR)
        st.markdown("### 第三關：我是小隊長")
        st.markdown("#### 指令： Tiyalen ko pising.")
        st.info("請問這個指令是要你做什麼動作？")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🙆‍♂️ 摸摸頭"):
                st.error("那是 Fongoh 喔！")
        with c2:
            if st.button("😊 摸摸臉頰"):
                st.snow()
                st.success("完全正確！Pising 是臉頰！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()

    else:
        # 結算畫面
        st.markdown(f"""
        <div style='text-align: center; padding: 50px;'>
            <h1>🏆 挑戰完成！ 🏆</h1>
            <h2>你的得分：{st.session_state.score} 分</h2>
            <p>你是阿美語小天才！</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
st.sidebar.title("導航列")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Designed for Grade 1-2 Amis Learning")
