import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# ==========================================
# 1. 系統配置
# ==========================================
st.set_page_config(
    page_title="Pangcah阿美語小教室",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 動態物理引擎 (The Magic)
# ==========================================
def inject_css_physics():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Fredoka:wght@500&display=swap');

    .stApp { background-color: #f4f7f6; font-family: 'Noto Sans TC', sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { padding-top: 1rem; max-width: 480px; }

    /* --- 定義動畫關鍵影格 (Keyframes) --- */
    
    /* 1. 搖頭晃腦 (Shake) - 用於頭、耳朵 */
    @keyframes shake {
        0% { transform: rotate(0deg); }
        25% { transform: rotate(10deg); }
        50% { transform: rotate(0deg); }
        75% { transform: rotate(-10deg); }
        100% { transform: rotate(0deg); }
    }

    /* 2. 眨眼 (Blink) - 用於眼睛 */
    @keyframes blink {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(0.1); }
    }

    /* 3. 彈跳 (Bounce) - 用於鼻子、嘴巴 */
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.3); }
    }

    /* 4. 擠壓 (Squeeze) - 用於臉頰 */
    @keyframes squeeze {
        0%, 100% { transform: scale(1, 1); }
        50% { transform: scale(1.1, 0.9); }
    }

    /* --- 卡片樣式 --- */
    .learn-card {
        background: white;
        border-radius: 20px;
        padding: 15px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.2s;
        border: 1px solid #eee;
    }
    .learn-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-color: #FFD700;
    }

    /* --- Emoji 動畫綁定類別 --- */
    .emoji-box {
        font-size: 45px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    /* 當滑鼠懸停在卡片上時，觸發動畫 */
    .learn-card:hover .anim-shake { animation: shake 0.5s ease-in-out infinite; }
    .learn-card:hover .anim-blink { animation: blink 0.3s ease-in-out 2; } /* 眨兩次 */
    .learn-card:hover .anim-bounce { animation: bounce 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) infinite; }
    .learn-card:hover .anim-squeeze { animation: squeeze 0.8s ease-in-out infinite; }

    /* 文字樣式 */
    .word-amis { font-family: 'Fredoka', sans-serif; font-size: 24px; font-weight: 600; color: #2c3e50; }
    .word-zh { font-size: 14px; color: #95a5a6; }
    
    /* 按鈕樣式 */
    .stButton > button {
        border-radius: 50px;
        height: 45px;
        border: none;
        background: #f0f2f6;
        color: #333;
        font-weight: bold;
    }
    .stButton > button:hover { background: #e1e4e8; }

    </style>
    """, unsafe_allow_html=True)

inject_css_physics()

# ==========================================
# 3. 數據層 (綁定 CSS 動畫類別)
# ==========================================
VOCABULARY = [
    {"amis": "Fongoh", "zh": "頭", "emoji": "💆‍♂️", "css": "anim-shake", "action": "摸摸頭"},
    {"amis": "Mata", "zh": "眼睛", "emoji": "👁️", "css": "anim-blink", "action": "眨眨眼"},
    {"amis": "Ngoso'", "zh": "鼻子", "emoji": "👃", "css": "anim-bounce", "action": "指鼻子"},
    {"amis": "Tangila", "zh": "耳朵", "emoji": "👂", "css": "anim-shake", "action": "拉耳朵"},
    {"amis": "Ngoyos", "zh": "嘴巴", "emoji": "👄", "css": "anim-bounce", "action": "張開嘴"},
    {"amis": "Pising", "zh": "臉頰", "emoji": "☺️", "css": "anim-squeeze", "action": "戳臉頰"}
]

# ==========================================
# 4. 音頻核心
# ==========================================
@st.cache_data(show_spinner=False)
def get_audio(text):
    try:
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except:
        return None

def play_sound(text):
    audio = get_audio(text)
    if audio:
        st.audio(audio, format='audio/mp3', start_time=0)

# ==========================================
# 5. 介面渲染
# ==========================================

st.title("Pangcah 小教室 ☀️")
st.caption("試著把滑鼠移到卡片上看看！")

tab1, tab2 = st.tabs(["📖 學習模式", "⚔️ 測驗模式"])

with tab1:
    st.markdown("### Unit 1: 我的身體")
    
    for idx, d in enumerate(VOCABULARY):
        # 使用 HTML 結構將 CSS 類別注入
        # 注意：我們將 emoji 包在一個 div 裡，並給予對應的 css class (如 anim-shake)
        card_html = f"""
        <div class="learn-card">
            <div>
                <div class="word-amis">{d['amis']}</div>
                <div class="word-zh">{d['zh']} ({d['action']})</div>
            </div>
            <div class="emoji-box {d['css']}">{d['emoji']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # 播放按鈕放在卡片下方，保持版面整潔
        if st.button(f"🔊 聽 {d['amis']}", key=f"play_{idx}"):
            play_sound(d['amis'])

with tab2:
    st.markdown("### ⚔️ 小勇士挑戰")
    if 'score' not in st.session_state: st.session_state.score = 0
    
    st.write(f"目前分數：{st.session_state.score}")
    
    if st.button("🎲 出題：聽聽看是哪個部位？"):
        target = VOCABULARY[0] # 簡單示範固定第一題，可改隨機
        play_sound(target['amis'])
        st.session_state.q = target
    
    if 'q' in st.session_state:
        st.write("請選擇正確的部位：")
        cols = st.columns(3)
        for i, opt in enumerate(VOCABULARY[:3]):
            with cols[i]:
                if st.button(opt['emoji']):
                    if opt['amis'] == st.session_state.q['amis']:
                        st.balloons()
                        st.success("答對了！")
                        st.session_state.score += 10
                    else:
                        st.error("不對喔！")

