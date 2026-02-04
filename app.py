import streamlit as st
import time
from gtts import gTTS
from io import BytesIO
import base64

# ==========================================
# 1. 核心配置與 CSS 注入 (System Layer)
# ==========================================
st.set_page_config(
    page_title="Pangcah阿美語小教室",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def inject_custom_css():
    st.markdown("""
    <style>
    /* 全局字體與背景 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Noto Sans TC', sans-serif;
    }

    /* 隱藏多餘元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 容器優化：手機端適配 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        max-width: 600px; /* 限制最大寬度，模擬 App 視窗 */
    }

    /* 卡片組件 (Glassmorphism) */
    .app-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.2s;
        text-align: center;
    }
    .app-card:active {
        transform: scale(0.98);
    }

    /* 標題樣式 */
    .word-title {
        font-size: 28px;
        font-weight: 800;
        color: #2c3e50;
        margin: 5px 0;
    }
    .word-sub {
        font-size: 16px;
        color: #7f8c8d;
        margin-bottom: 10px;
    }
    .action-badge {
        background-color: #e1f5fe;
        color: #0288d1;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
    }

    /* 按鈕重構 */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    /* 主要按鈕 (Primary) */
    .primary-btn {
        background: linear-gradient(45deg, #FFD700, #FFC107);
        color: #333;
    }
    
    /* 選項按鈕樣式 */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }

    /* 進度條優化 */
    .stProgress > div > div > div > div {
        background-color: #2ECC71;
    }
    
    /* 底部導航模擬 */
    .bottom-nav-spacer {
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ==========================================
# 2. 數據層 (Data Layer)
# ==========================================
# 使用 Session State 管理全局狀態，防止刷新重置
class StateManager:
    @staticmethod
    def init():
        if 'xp' not in st.session_state: st.session_state.xp = 0
        if 'level' not in st.session_state: st.session_state.level = 1
        if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
        if 'streak' not in st.session_state: st.session_state.streak = 0

    @staticmethod
    def add_xp(amount):
        st.session_state.xp += amount
        # 簡單的升級邏輯：每 300 XP 升一級
        new_level = (st.session_state.xp // 300) + 1
        if new_level > st.session_state.level:
            st.session_state.level = new_level
            st.toast(f"🎉 恭喜升級！現在是 Lv.{new_level}", icon="🆙")
        st.session_state.streak += 1

    @staticmethod
    def reset_quiz():
        st.session_state.quiz_step = 0

StateManager.init()

VOCABULARY = [
    {"amis": "Fongoh", "zh": "頭", "emoji": "💆‍♂️", "action": "摸摸頭", "audio_key": "fongoh"},
    {"amis": "Mata", "zh": "眼睛", "emoji": "👁️", "action": "眨眨眼", "audio_key": "mata"},
    {"amis": "Ngoso'", "zh": "鼻子", "emoji": "👃", "action": "指鼻子", "audio_key": "ngoso"},
    {"amis": "Tangila", "zh": "耳朵", "emoji": "👂", "action": "拉耳朵", "audio_key": "tangila"},
    {"amis": "Ngoyos", "zh": "嘴巴", "emoji": "👄", "action": "張開嘴", "audio_key": "ngoyos"},
    {"amis": "Pising", "zh": "臉頰", "emoji": "☺️", "action": "戳臉頰", "audio_key": "pising"}
]

# ==========================================
# 3. 服務層 (Service Layer) - 性能核心
# ==========================================
# 使用 cache_data 確保語音只生成一次，大幅提升響應速度
@st.cache_data(show_spinner=False)
def get_audio_html(text, lang='id'):
    """生成隱藏的音頻播放器 HTML，避免阻塞 UI"""
    try:
        tts = gTTS(text=text, lang=lang)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        # 自動播放的 HTML
        return f"""
            <audio controls autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
    except Exception as e:
        return ""

def play_sound(text):
    """在 UI 中注入音頻"""
    audio_html = get_audio_html(text)
    st.markdown(audio_html, unsafe_allow_html=True)

# ==========================================
# 4. UI 組件層 (Component Layer)
# ==========================================
def header_component():
    """頂部狀態欄"""
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(f"**☀️ Pangcah 小教室**")
    with c2:
        st.markdown(f"🔥 {st.session_state.streak}")
    with c3:
        st.markdown(f"⭐ Lv.{st.session_state.level}")
    st.progress(min(100, st.session_state.xp % 300 / 300))

def word_card(word_data):
    """單詞卡片組件"""
    # 使用 container 模擬點擊區域
    with st.container():
        st.markdown(f"""
        <div class="app-card">
            <div style="font-size: 48px; margin-bottom: 10px;">{word_data['emoji']}</div>
            <div class="word-title">{word_data['amis']}</div>
            <div class="word-sub">{word_data['zh']}</div>
            <div class="action-badge">動作：{word_data['action']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 播放按鈕獨立，避免整張卡片觸發重繪
        if st.button(f"🔊 聽發音", key=f"btn_{word_data['amis']}"):
            play_sound(word_data['amis'])

# ==========================================
# 5. 業務邏輯層 (Business Logic Layer)
# ==========================================

def render_learning_mode():
    st.markdown("### 📖 單詞學習 (Unit 1)")
    
    # 響應式網格佈局
    col1, col2 = st.columns(2)
    for idx, word in enumerate(VOCABULARY):
        with (col1 if idx % 2 == 0 else col2):
            word_card(word)
            
    st.markdown("---")
    st.markdown("### 🗣️ 句型跟讀")
    
    sentences = [
        ("O maan koni?", "這是什麼？"),
        ("O Mata koni.", "這是眼睛。")
    ]
    
    for s_amis, s_zh in sentences:
        st.info(f"**{s_amis}**\n\n{s_zh}")
        if st.button(f"▶️ 播放", key=s_amis):
            play_sound(s_amis)

def render_quiz_mode():
    st.markdown("### 🏆 小勇士挑戰")
    
    step = st.session_state.quiz_step
    
    if step == 0:
        st.markdown(f"""
        <div class="app-card">
            <h3>👂 聽力測驗</h3>
            <p>請點擊下方按鈕聽聲音，然後選出正確的身體部位。</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔊 播放題目聲音"):
            play_sound("Tangila")
            
        st.write("")
        cols = st.columns(2)
        with cols[0]:
            if st.button("👃 鼻子"):
                st.error("不對喔，那是 Ngoso'")
        with cols[1]:
            if st.button("👂 耳朵"):
                play_sound("Nga'ay ho!") # 答對音效
                st.balloons()
                st.success("答對了！Tangila 是耳朵！")
                time.sleep(1.5)
                StateManager.add_xp(50)
                st.session_state.quiz_step = 1
                st.rerun()
                
        cols2 = st.columns(2)
        with cols2[0]:
            if st.button("👁️ 眼睛"): st.error("不對喔，那是 Mata")
        with cols2[1]:
            if st.button("👄 嘴巴"): st.error("不對喔，那是 Ngoyos")

    elif step == 1:
        st.markdown(f"""
        <div class="app-card">
            <h3>👄 口說理解</h3>
            <p>當別人問：<b>"O maan koni?"</b> (這是什麼？)</p>
            <p>指著 <span style="font-size:30px">👄</span> 時，你要怎麼回答？</p>
        </div>
        """, unsafe_allow_html=True)
        
        options = ["O Fongoh koni.", "O Ngoyos koni.", "O Pising koni."]
        choice = st.radio("請選擇正確的回答：", options)
        
        if st.button("✅ 提交答案"):
            if "Ngoyos" in choice:
                play_sound("O Ngoyos koni")
                st.snow()
                st.success("太棒了！")
                time.sleep(1.5)
                StateManager.add_xp(50)
                st.session_state.quiz_step = 2
                st.rerun()
            else:
                st.error("再想一下喔！")

    elif step == 2:
        st.markdown(f"""
        <div class="app-card" style="background: #FFF8E1; border: 2px solid #FFD700;">
            <h1>🎉 挑戰成功！</h1>
            <h3>本單元 XP +100</h3>
            <p>你已經學會了身體部位囉！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            StateManager.reset_quiz()
            st.rerun()

# ==========================================
# 6. 主程序 (Main Execution)
# ==========================================
header_component()

# 使用 Tabs 進行頂層導航
tab_learn, tab_quiz = st.tabs(["📚 學習單詞", "⚔️ 闖關挑戰"])

with tab_learn:
    render_learning_mode()

with tab_quiz:
    render_quiz_mode()

# 底部留白，防止手機端內容被遮擋
st.markdown('<div class="bottom-nav-spacer"></div>', unsafe_allow_html=True)
