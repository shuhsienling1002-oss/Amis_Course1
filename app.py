import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# ==========================================
# 1. 系統核心配置 (System Kernel)
# ==========================================
st.set_page_config(
    page_title="Pangcah阿美語小教室 Pro",
    page_icon="☀️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS 注入：打造原生 App 級別的視覺層次 ---
def inject_pro_css():
    st.markdown("""
    <style>
    /* 引入圓體字型，增加親和力 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;700&family=Varela+Round&display=swap');

    .stApp {
        background-color: #f4f7f6;
        font-family: 'Noto Sans TC', sans-serif;
    }

    /* 隱藏干擾元素 */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* 手機視圖容器優化 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 4rem !important;
        max-width: 480px; /* 嚴格限制寬度，模擬手機 */
    }

    /* --- 組件：教學卡片 (Learning Card) --- */
    .learn-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 6px solid #FFD700; /* 阿美族代表色點綴 */
        transition: transform 0.2s;
    }
    .learn-card:hover { transform: translateY(-2px); }
    
    .card-header { display: flex; align-items: center; justify-content: space-between; }
    .card-emoji { font-size: 40px; }
    .card-title { font-size: 24px; font-weight: 800; color: #333; font-family: 'Varela Round'; }
    .card-sub { font-size: 16px; color: #666; font-weight: 500; }
    .card-action { 
        background: #e0f7fa; color: #006064; 
        padding: 4px 10px; border-radius: 12px; 
        font-size: 12px; font-weight: bold; margin-top: 8px; display: inline-block;
    }

    /* --- 組件：句型氣泡 (Sentence Bubble) --- */
    .sentence-box {
        background: #fff;
        border-radius: 18px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #eee;
        position: relative;
    }
    .sentence-amis { color: #2E86C1; font-weight: bold; font-size: 18px; }
    .sentence-zh { color: #888; font-size: 14px; margin-top: 4px; }

    /* --- 組件：交互按鈕 (Interactive Button) --- */
    .stButton > button {
        width: 100%;
        border-radius: 50px; /* 膠囊型按鈕 */
        height: 54px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    /* 主要操作按鈕 */
    div[data-testid="stVerticalBlock"] > div > div > div > div > .stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #FFC107 100%);
        color: #333;
    }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div { background-color: #2ECC71; }
    </style>
    """, unsafe_allow_html=True)

inject_pro_css()

# ==========================================
# 2. 數據結構層 (Data Structure Layer)
# ==========================================
# 保留原本的完整結構，並增加 metadata
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "💆‍♂️", "action": "摸摸頭", "type": "body"},
    "Mata":     {"zh": "眼睛", "emoji": "👁️", "action": "眨眨眼", "type": "face"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "action": "指鼻子", "type": "face"}, 
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "action": "拉耳朵", "type": "face"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "action": "張開嘴", "type": "face"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "☺️", "action": "戳臉頰", "type": "face"}
}

SENTENCES = [
    {"id": "q_what", "amis": "O maan koni?", "zh": "這是什麼？", "type": "question"},
    {"id": "a_mata", "amis": "O {word} koni.", "zh": "這是{word}。", "type": "answer"}, 
    {"id": "cmd_close", "amis": "Piti'en ko mata.", "zh": "閉上眼睛。", "type": "command"},
    {"id": "cmd_touch", "amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。", "type": "command"}
]

# ==========================================
# 3. 核心邏輯層 (Core Logic & Cache)
# ==========================================

class AudioManager:
    """音頻管理單元：負責生成、緩存與播放"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def generate_audio(text, lang='id'):
        """生成音頻二進制數據並緩存"""
        try:
            tts = gTTS(text=text, lang=lang)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except:
            return None

    @staticmethod
    def play(text, key_suffix=""):
        """播放接口"""
        audio_data = AudioManager.generate_audio(text)
        if audio_data:
            # 使用 key 避免組件衝突
            st.audio(audio_data, format='audio/mp3', start_time=0)

class QuizEngine:
    """測驗狀態機：管理關卡邏輯"""
    
    @staticmethod
    def init_state():
        if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 0
        if 'score' not in st.session_state: st.session_state.score = 0
        if 'feedback' not in st.session_state: st.session_state.feedback = None

    @staticmethod
    def next_step(points=0):
        st.session_state.score += points
        st.session_state.quiz_step += 1
        st.rerun()

    @staticmethod
    def reset():
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.session_state.feedback = None
        st.rerun()

QuizEngine.init_state()

# ==========================================
# 4. 視圖層 (View Layer) - 模組化渲染
# ==========================================

def render_learning_mode():
    """學習模式：展示單詞與句型"""
    st.markdown("### 📚 Unit 1: 我的身體")
    st.info("💡 點擊卡片上的按鈕聆聽發音")

    # --- Part 1: 單詞卡片流 ---
    for amis, data in VOCABULARY.items():
        col_text, col_btn = st.columns([3, 1])
        
        # 使用 HTML 構建精美卡片
        st.markdown(f"""
        <div class="learn-card">
            <div class="card-header">
                <div>
                    <div class="card-emoji">{data['emoji']}</div>
                    <div class="card-title">{amis}</div>
                    <div class="card-sub">{data['zh']}</div>
                    <div class="card-action">動作：{data['action']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 獨立的播放按鈕，避免重繪整個卡片
        if st.button(f"🔊", key=f"btn_learn_{amis}"):
            AudioManager.play(amis)

    st.markdown("---")
    st.markdown("### 🗣️ 句型對話練習")

    # --- Part 2: 句型對話流 ---
    # Q: 這是什麼？
    s1 = SENTENCES[0]
    st.markdown(f"""
    <div class="sentence-box" style="border-left: 5px solid #3498DB;">
        <div class="sentence-amis">Q: {s1['amis']}</div>
        <div class="sentence-zh">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔊 播放問句", key="btn_s1"): AudioManager.play(s1['amis'])

    # A: 這是眼睛
    s2_text = SENTENCES[1]['amis'].format(word="Mata")
    st.markdown(f"""
    <div class="sentence-box" style="border-left: 5px solid #F1C40F;">
        <div class="sentence-amis">A: {s2_text}</div>
        <div class="sentence-zh">這是眼睛。</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔊 播放答句", key="btn_s2"): AudioManager.play(s2_text)

def render_quiz_mode():
    """測驗模式：狀態機驅動的闖關體驗"""
    
    # 進度條
    total_steps = 3
    progress = min(st.session_state.quiz_step / total_steps, 1.0)
    st.progress(progress)
    
    step = st.session_state.quiz_step

    # --- 狀態 0: 聽力辨識 (單詞) ---
    if step == 0:
        st.markdown("### 👂 第 1 關：聽音辨位")
        st.markdown("請聽語音，選出正確的身體部位：")
        
        target = "Tangila" # 耳朵
        
        # 自動播放 (UX 優化：進入關卡自動讀題)
        st.caption("正在播放題目...")
        AudioManager.play(target, key_suffix="q1")
        
        st.write("") # Spacer
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👃 鼻子", key="q1_opt1"): st.error("那是 Ngoso' 喔！")
        with c2:
            if st.button("👂 耳朵", key="q1_opt2"): 
                st.toast("✅ 答對了！ Tangila 是耳朵", icon="🎉")
                time.sleep(1)
                QuizEngine.next_step(100)
        with c3:
            if st.button("👁️ 眼睛", key="q1_opt3"): st.error("那是 Mata 喔！")

    # --- 狀態 1: 句型填空 (邏輯) ---
    elif step == 1:
        st.markdown("### 🧩 第 2 關：句型填空")
        st.markdown("當別人問：**O maan koni?** (這是什麼？)")
        st.markdown("你要回答：**O ______ koni.** (指著嘴巴 👄)")
        
        st.image("https://tw.pseg.com/wp-content/uploads/2020/06/mouth-icon.png", width=100) # 示意圖
        
        options = ["Fongoh (頭)", "Ngoyos (嘴巴)", "Pising (臉)"]
        choice = st.radio("請選擇正確的單詞：", options)
        
        if st.button("送出答案", key="q2_submit"):
            if "Ngoyos" in choice:
                st.balloons()
                st.success("Correct! O Ngoyos koni.")
                time.sleep(1.5)
                QuizEngine.next_step(100)
            else:
                st.error("再想一下，嘴巴是哪個詞？")

    # --- 狀態 2: TPR 全身反應 (指令) ---
    elif step == 2:
        st.markdown("### 🏃 第 3 關：我是小隊長")
        st.markdown("聽到指令後，請確認動作：")
        
        cmd = "Dihdihen ko pising"
        st.markdown(f"<h2 style='text-align:center; color:#E74C3C'>{cmd}</h2>", unsafe_allow_html=True)
        
        if st.button("🔊 播放指令", key="btn_q3_audio"):
            AudioManager.play(cmd)
            
        st.info("這個指令是什麼意思？")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("摸摸頭", key="q3_opt1"): st.error("不對喔，Fongoh 才是頭")
        with col2:
            if st.button("摸摸臉頰", key="q3_opt2"):
                st.snow()
                QuizEngine.next_step(100)

    # --- 狀態 3: 結算畫面 ---
    else:
        st.markdown(f"""
        <div style="background:#FFF8E1; padding:30px; border-radius:20px; text-align:center; border: 2px dashed #FFC107;">
            <h1>🏆 挑戰成功！</h1>
            <h2 style="color:#D35400">總分：{st.session_state.score} / 300</h2>
            <p>你的阿美語越來越厲害了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 再玩一次", key="btn_restart"):
            QuizEngine.reset()

# ==========================================
# 5. 主程式入口 (Main Entry)
# ==========================================

st.title("Pangcah 小教室 ☀️")

# 使用 Tabs 保持結構清晰，但內容不減
tab1, tab2 = st.tabs(["📖 學習模式", "⚔️ 闖關挑戰"])

with tab1:
    render_learning_mode()

with tab2:
    render_quiz_mode()
