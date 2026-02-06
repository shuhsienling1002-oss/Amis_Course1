import streamlit as st
import time
import requests
from gtts import gTTS
from io import BytesIO
from streamlit_lottie import st_lottie

# ==========================================
# 1. 系統核心配置 (System Kernel)
# ==========================================
st.set_page_config(
    page_title="Pangcah阿美語小教室 Pro",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS 注入：動態質感優化 ---
def inject_pro_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Varela+Round&display=swap');

    .stApp {
        background-color: #f8f9fa;
        font-family: 'Noto Sans TC', sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 4rem !important;
        max-width: 480px;
    }

    /* 卡片樣式 */
    .learn-card {
        background: white;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .learn-card:hover { transform: translateY(-3px); }
    
    .card-title { font-size: 24px; font-weight: 800; color: #2c3e50; font-family: 'Varela Round'; }
    .card-sub { font-size: 16px; color: #95a5a6; font-weight: 500; }
    .card-action { 
        background: #e3f2fd; color: #1565c0; 
        padding: 4px 12px; border-radius: 12px; 
        font-size: 12px; font-weight: bold; margin-top: 8px; display: inline-block;
    }

    /* 按鈕樣式 */
    .stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: all 0.2s;
    }
    .stButton > button:active { transform: scale(0.97); }
    
    /* 句型框 */
    .sentence-box {
        background: #fff;
        border-radius: 16px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #ddd;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

inject_pro_css()

# ==========================================
# 2. 資源管理層 (Lottie & Audio)
# ==========================================

class ResourceManager:
    """統一管理外部資源 (動畫與音頻)"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_lottie(url):
        """加載 Lottie 動畫 JSON"""
        try:
            r = requests.get(url)
            if r.status_code != 200: return None
            return r.json()
        except:
            return None

    @staticmethod
    @st.cache_data(show_spinner=False)
    def generate_audio(text, lang='id'):
        """生成並緩存音頻"""
        try:
            tts = gTTS(text=text, lang=lang)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except:
            return None

    @staticmethod
    def play_audio(text):
        """播放音頻接口"""
        audio_data = ResourceManager.generate_audio(text)
        if audio_data:
            st.audio(audio_data, format='audio/mp3', start_time=0)

    @staticmethod
    def show_lottie(url, height=150, key=None):
        """渲染 Lottie 動畫"""
        lottie_json = ResourceManager.load_lottie(url)
        if lottie_json:
            st_lottie(lottie_json, height=height, key=key)
        else:
            st.error("動畫加載失敗")

# --- 數據定義 (混合了 Emoji 和 Lottie URL) ---
# 為了示範，我將 "Fongoh" 設為動態，其他保持 Emoji
VOCABULARY = [
    {
        "amis": "Fongoh", "zh": "頭", 
        "emoji": "💆‍♂️", 
        "lottie": "https://lottie.host/5a092822-13f5-47f6-a7f4-279549495147/o3Xz7y2g3P.json", # 動態資源
        "action": "摸摸頭"
    },
    {
        "amis": "Mata", "zh": "眼睛", 
        "emoji": "👁️", 
        "lottie": None, 
        "action": "眨眨眼"
    },
    {
        "amis": "Ngoso'", "zh": "鼻子", 
        "emoji": "👃", 
        "lottie": None, 
        "action": "指鼻子"
    },
    {
        "amis": "Tangila", "zh": "耳朵", 
        "emoji": "👂", 
        "lottie": None, 
        "action": "拉耳朵"
    },
    {
        "amis": "Ngoyos", "zh": "嘴巴", 
        "emoji": "👄", 
        "lottie": None, 
        "action": "張開嘴"
    },
    {
        "amis": "Pising", "zh": "臉頰", 
        "emoji": "☺️", 
        "lottie": None, 
        "action": "戳臉頰"
    }
]

SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？"},
    {"amis": "O {word} koni.", "zh": "這是{word}。"}, 
]

# 慶祝動畫 URL
ANIM_SUCCESS = "https://lottie.host/81729a4d-0839-4467-8438-232537901726/H2a6j9q9k9.json"

# ==========================================
# 3. 業務邏輯層 (Logic & State)
# ==========================================

class QuizEngine:
    """測驗狀態機"""
    @staticmethod
    def init():
        if 'step' not in st.session_state: st.session_state.step = 0
        if 'score' not in st.session_state: st.session_state.score = 0

    @staticmethod
    def next_level(points=0):
        st.session_state.score += points
        st.session_state.step += 1
        st.rerun()

    @staticmethod
    def reset():
        st.session_state.step = 0
        st.session_state.score = 0
        st.rerun()

QuizEngine.init()

# ==========================================
# 4. 視圖層 (View Layer)
# ==========================================

def render_learning():
    st.markdown("### 📚 Unit 1: 我的身體")
    st.caption("點擊 🔊 聽發音")

    for idx, data in enumerate(VOCABULARY):
        # 卡片容器
        with st.container():
            st.markdown(f"""
            <div class="learn-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="card-title">{data['amis']}</div>
                        <div class="card-sub">{data['zh']}</div>
                        <div class="card-action">{data['action']}</div>
                    </div>
                    <div style="width: 80px; text-align:center; font-size:40px;">
                        <!-- 這裡留空，由下方 Python 邏輯決定填入 Lottie 或 Emoji -->
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 佈局：左邊放動畫/Emoji，右邊放播放按鈕
            c1, c2 = st.columns([3, 1])
            with c1:
                # 判斷是否有 Lottie 資源
                if data.get('lottie'):
                    ResourceManager.show_lottie(data['lottie'], height=100, key=f"anim_{idx}")
                else:
                    # 如果沒有 Lottie，顯示大 Emoji
                    st.markdown(f"<div style='font-size:60px; text-align:center; margin-top:-80px; margin-left: 180px; position:relative; pointer-events:none;'>{data['emoji']}</div>", unsafe_allow_html=True)
            
            with c2:
                st.write("") # Spacer
                if st.button("🔊", key=f"play_{idx}"):
                    ResourceManager.play_audio(data['amis'])

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    st.markdown(f"""
    <div class="sentence-box" style="border-color: #3498DB;">
        <div style="color:#2980B9; font-weight:bold;">Q: {s1['amis']}</div>
        <div style="color:#7f8c8d; font-size:14px;">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("播放問句", key="s1"): ResourceManager.play_audio(s1['amis'])

def render_quiz():
    step = st.session_state.step
    st.progress(min(step / 3, 1.0))

    if step == 0:
        st.markdown("### 👂 第 1 關：聽音辨位")
        st.info("請聽語音，選出正確的部位")
        
        target = "Tangila"
        st.caption("正在播放...")
        ResourceManager.play_audio(target)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👃 鼻子", key="q1_1"): st.error("那是 Ngoso'")
            if st.button("👂 耳朵", key="q1_2"):
                st.toast("Correct!", icon="🎉")
                QuizEngine.next_level(100)
        with c2:
            if st.button("👁️ 眼睛", key="q1_3"): st.error("那是 Mata")
            if st.button("👄 嘴巴", key="q1_4"): st.error("那是 Ngoyos")

    elif step == 1:
        st.markdown("### 🧩 第 2 關：填空題")
        st.markdown("**Q: O maan koni?**")
        st.markdown("**A: O ______ koni.** (指著嘴巴)")
        
        # 這裡也可以放個嘴巴的 Lottie
        st.markdown("<div style='font-size:60px; text-align:center;'>👄</div>", unsafe_allow_html=True)
        
        opts = ["Fongoh", "Ngoyos", "Pising"]
        choice = st.radio("選擇單詞：", opts)
        
        if st.button("送出答案"):
            if choice == "Ngoyos":
                st.balloons()
                # 播放慶祝動畫
                ResourceManager.show_lottie(ANIM_SUCCESS, height=200, key="win_q2")
                time.sleep(2)
                QuizEngine.next_level(100)
            else:
                st.error("再試一次！")

    elif step == 2:
        st.markdown("### 🏆 挑戰成功")
        st.markdown(f"<h1 style='text-align:center; color:#F1C40F;'>得分: {st.session_state.score}</h1>", unsafe_allow_html=True)
        
        # 巨大的慶祝動畫
        ResourceManager.show_lottie(ANIM_SUCCESS, height=300, key="win_final")
        
        if st.button("🔄 再玩一次"):
            QuizEngine.reset()

# ==========================================
# 5. 主程式入口
# ==========================================

st.title("Pangcah 小教室 Pro")
tab1, tab2 = st.tabs(["📖 學習模式", "⚔️ 闖關挑戰"])

with tab1:
    render_learning()
with tab2:
    render_quiz()
