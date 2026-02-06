import streamlit as st
import time
import random
from gtts import gTTS
from io import BytesIO

# ==========================================
# 1. 系統層 (System Layer) - 配置與 CSS
# ==========================================
st.set_page_config(
    page_title="Pangcah 小教室",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    st.markdown("""
    <style>
    /* --- 全局字體與背景 (Mobile Friendly) --- */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Fredoka:wght@500&display=swap');
    
    .stApp {
        background: linear-gradient(160deg, #fdfbfb 0%, #ebedee 100%);
        font-family: 'Noto Sans TC', sans-serif;
    }

    /* --- 隱藏 Streamlit 原生元素 --- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* --- 容器優化 --- */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        max-width: 500px; /* 限制寬度，模擬手機視窗 */
    }

    /* --- 卡片組件 (Neumorphism / Soft UI) --- */
    .word-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border: 1px solid #f0f0f0;
        text-align: center;
        transition: transform 0.2s;
    }
    .word-card:active {
        transform: scale(0.98);
    }
    
    .emoji-big { font-size: 48px; margin-bottom: 8px; }
    .text-amis { font-family: 'Fredoka', sans-serif; font-size: 28px; font-weight: 600; color: #2c3e50; }
    .text-zh { font-size: 16px; color: #95a5a6; margin-bottom: 12px; }
    .action-tag { 
        background: #e3f2fd; color: #1976d2; 
        padding: 4px 12px; border-radius: 20px; 
        font-size: 12px; font-weight: bold;
        display: inline-block;
    }

    /* --- 按鈕優化 (Fitts's Law) --- */
    .stButton > button {
        width: 100%;
        height: 55px;
        border-radius: 16px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.2s;
    }
    
    /* 答題按鈕特效 */
    .stButton > button:active {
        transform: scale(0.96);
    }

    /* --- 頂部狀態列 --- */
    .stats-container {
        display: flex;
        justify-content: space-between;
        background: white;
        padding: 10px 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .stat-item { font-weight: bold; color: #555; }
    .stat-value { color: #FFD700; font-size: 1.2em; }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==========================================
# 2. 數據與狀態層 (Data & State Layer)
# ==========================================

# 詞彙庫 (擴展容易)
VOCABULARY = [
    {"amis": "Fongoh", "zh": "頭", "emoji": "💆‍♂️", "action": "摸摸頭"},
    {"amis": "Mata", "zh": "眼睛", "emoji": "👁️", "action": "眨眨眼"},
    {"amis": "Ngoso'", "zh": "鼻子", "emoji": "👃", "action": "指鼻子"},
    {"amis": "Tangila", "zh": "耳朵", "emoji": "👂", "action": "拉耳朵"},
    {"amis": "Ngoyos", "zh": "嘴巴", "emoji": "👄", "action": "張開嘴"},
    {"amis": "Pising", "zh": "臉頰", "emoji": "☺️", "action": "戳臉頰"}
]

# 初始化 Session State
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'level' not in st.session_state: st.session_state.level = 1
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'quiz_mode' not in st.session_state: st.session_state.quiz_mode = False
if 'current_q' not in st.session_state: st.session_state.current_q = None

# ==========================================
# 3. 資源層 (Resource Layer) - 緩存與音頻
# ==========================================

@st.cache_data(show_spinner=False)
def get_audio_bytes(text, lang='id'):
    """
    使用緩存機制生成音頻，避免重複調用 API。
    選用 'id' (印尼語) 是因為發音結構與阿美語較接近。
    """
    try:
        tts = gTTS(text=text, lang=lang)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except:
        return None

def play_audio_native(text):
    """使用 Streamlit 原生播放器 (最穩定)"""
    audio_bytes = get_audio_bytes(text)
    if audio_bytes:
        # autoplay=True 需要 Streamlit 1.33+
        st.audio(audio_bytes, format='audio/mp3', autoplay=True)

# ==========================================
# 4. 組件層 (Component Layer)
# ==========================================

def render_header():
    """顯示頂部狀態欄"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"🏆 Lv.{st.session_state.level}")
    with col2:
        st.markdown(f"🔥 連勝 {st.session_state.streak}")
    with col3:
        st.markdown(f"⭐ XP {st.session_state.xp}")
    st.progress(min((st.session_state.xp % 100) / 100, 1.0))

def render_word_card(word_data):
    """渲染單詞卡片"""
    st.markdown(f"""
    <div class="word-card">
        <div class="emoji-big">{word_data['emoji']}</div>
        <div class="text-amis">{word_data['amis']}</div>
        <div class="text-zh">{word_data['zh']}</div>
        <div class="action-tag">動作：{word_data['action']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 播放按鈕 (全寬)
    if st.button(f"🔊 聽發音 ({word_data['amis']})", key=f"btn_{word_data['amis']}"):
        play_audio_native(word_data['amis'])

# ==========================================
# 5. 業務邏輯層 (Logic Layer)
# ==========================================

def tab_learning():
    """學習模式"""
    st.markdown("### 📖 單詞卡")
    
    # 使用網格佈局 (手機上會自動變單列)
    for word in VOCABULARY:
        render_word_card(word)

def tab_quiz():
    """測驗模式 (遊戲化核心)"""
    st.markdown("### ⚔️ 小勇士挑戰")
    
    if st.button("🎲 開始新挑戰 / 下一題", type="primary"):
        st.session_state.current_q = random.choice(VOCABULARY)
        # 清除之前的音頻播放狀態 (透過 rerun)
        st.rerun()

    if st.session_state.current_q:
        q = st.session_state.current_q
        
        st.markdown(f"""
        <div style="text-align:center; padding: 20px;">
            <h3>請聽音頻，選擇正確的意思</h3>
            <div style="font-size: 60px;">🔊</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 自動播放題目音頻
        play_audio_native(q['amis'])
        
        # 生成選項 (1個正確 + 2個干擾)
        options = [q]
        distractors = [w for w in VOCABULARY if w['amis'] != q['amis']]
        options.extend(random.sample(distractors, 2))
        random.shuffle(options)
        
        # 顯示選項
        st.write("")
        cols = st.columns(3)
        for i, opt in enumerate(options):
            # 手機上 columns 會變窄，這裡直接用按鈕
            if st.button(f"{opt['emoji']} {opt['zh']}", key=f"quiz_{i}"):
                if opt['amis'] == q['amis']:
                    st.toast("🎉 答對了！+20 XP", icon="✅")
                    st.session_state.xp += 20
                    st.session_state.streak += 1
                    st.balloons()
                    
                    # 升級邏輯
                    if st.session_state.xp >= st.session_state.level * 100:
                        st.session_state.level += 1
                        st.toast(f"🆙 升級了！現在是 Lv.{st.session_state.level}", icon="🚀")
                    
                    time.sleep(1)
                    st.rerun()
                else:
                    st.toast("😢 答錯了，連勝中斷...", icon="❌")
                    st.session_state.streak = 0
                    st.error(f"正確答案是：{q['zh']} ({q['amis']})")

# ==========================================
# 6. 主程式入口 (Main Entry)
# ==========================================

render_header()

tab1, tab2 = st.tabs(["📚 學習單詞", "🎯 聽力測驗"])

with tab1:
    tab_learning()

with tab2:
    tab_quiz()
