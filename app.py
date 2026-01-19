import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心功能函數 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式 (模擬發音)"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 模擬南島語系發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音無法播放)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 1: O Tireng", page_icon="🙆‍♂️", layout="centered")

# --- CSS 手機版面優化 (參照 Unit 31-40 風格) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #FFCCBC; color: #BF360C; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 - 手機友善 */
    .word-card {
        background: linear-gradient(135deg, #FFEBEE 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FF7043;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 24px; font-weight: bold; color: #D84315; } /* 字體加大 */
    .chinese-text { font-size: 18px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFEBEE;
        border-left: 5px solid #FF7043;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 - 手機好點擊 (加高) */
    .stButton>button {
        width: 100%; 
        border-radius: 12px; 
        font-size: 22px; 
        font-weight: 600;
        background-color: #FFCCBC; 
        color: #BF360C; 
        border: 2px solid #D84315; 
        padding: 15px 12px; /* 增加高度 */
        margin-top: 10px;
    }
    .stButton>button:hover { background-color: #FFAB91; border-color: #BF360C; }
    .stProgress > div > div > div > div { background-color: #D84315; }
    
    /* 選項按鈕優化 */
    div[role="radiogroup"] > label > div:first-of-type {
        display: none; /* 隱藏原本的圈圈，改用按鈕樣式 (Streamlit原生限制較多，此為輔助) */
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 1: 身體部位) ---
vocab_data = [
    {"amis": "Fongoh", "chi": "頭", "icon": "🙆‍♂️", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Mata", "chi": "眼睛", "icon": "👀", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Ngoso'", "chi": "鼻子", "icon": "👃", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Tangila", "chi": "耳朵", "icon": "👂", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Ngoyos", "chi": "嘴巴", "icon": "👄", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Pising", "chi": "臉 / 臉頰", "icon": "😊", "source": "Unit 1", "morph": "Noun"},
    {"amis": "Fokes", "chi": "頭髮", "icon": "💇", "source": "Ext.", "morph": "Noun"},
    {"amis": "Tireng", "chi": "身體", "icon": "💪", "source": "Ext.", "morph": "Noun"},
    {"amis": "Kamay", "chi": "手", "icon": "✋", "source": "Ext.", "morph": "Noun"},
    {"amis": "Wa'ay", "chi": "腳", "icon": "🦶", "source": "Ext.", "morph": "Noun"},
]

# --- 句子庫 ---
sentences = [
    {"amis": "O maan koni?", "chi": "這是什麼？", "icon": "❓", "source": "Unit 1"},
    {"amis": "O mata koni.", "chi": "這是眼睛。", "icon": "👀", "source": "Unit 1"},
    {"amis": "Piti'en ko mata.", "chi": "閉上眼睛。", "icon": "😌", "source": "Unit 1"},
    {"amis": "Dihdihen ko pising.", "chi": "摸摸臉頰。", "icon": "👉", "source": "Unit 1"},
    {"amis": "Adada ko fongoh.", "chi": "頭痛。", "icon": "🤕", "source": "Ext."},
]

# --- 3. 隨機題庫 (包含聽力、字義) ---
raw_quiz_pool = [
    {
        "q": "O maan koni? (看圖回答)",
        "audio": "O maan koni?",
        "options": ["O mata (是眼睛)", "O ngoso' (是鼻子)", "O fongoh (是頭)"],
        "ans": "O mata (是眼睛)",
        "hint": "Mata = 眼睛"
    },
    {
        "q": "單字測驗：Tangila",
        "audio": "Tangila",
        "options": ["耳朵", "嘴巴", "手"],
        "ans": "耳朵",
        "hint": "用來聽聲音的部位"
    },
    {
        "q": "單字測驗：Ngoyos",
        "audio": "Ngoyos",
        "options": ["嘴巴", "鼻子", "臉"],
        "ans": "嘴巴",
        "hint": "吃東西的地方"
    },
    {
        "q": "Piti'en ko mata.",
        "audio": "Piti'en ko mata",
        "options": ["閉上眼睛", "張開眼睛", "摸摸眼睛"],
        "ans": "閉上眼睛",
        "hint": "Piti'en = 閉上"
    },
    {
        "q": "單字測驗：Fongoh",
        "audio": "Fongoh",
        "options": ["頭", "頭髮", "脖子"],
        "ans": "頭",
        "hint": "最上面的部位"
    },
    {
        "q": "Dihdihen ko pising.",
        "audio": "Dihdihen ko pising",
        "options": ["摸摸臉頰", "洗洗臉", "拍拍手"],
        "ans": "摸摸臉頰",
        "hint": "Dihdihen = 按摩/摸"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯：一次抽 3 題) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 這裡依照您的指示：一次出 3 題
    selected_questions = random.sample(raw_quiz_pool, 3)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 (Tabs 設計) ---
st.markdown("<h1 style='text-align: center; color: #D84315;'>Unit 1: O Tireng</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>我的身體 (手機版面)</p>", unsafe_allow_html=True)

# 這裡使用 Tabs，這是您最習慣的 31-40 設計方式
tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字")
    # 手機上 columns(2) 會自動並排或堆疊，視螢幕寬度而定
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #D84315;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 (3題) ===
with tab2:
    st.markdown("### 🎲 隨機評量 (共3題)")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        # 進度條 (分母為 3)
        st.progress((st.session_state.current_q_idx) / 3)
        st.markdown(f"**第 {st.session_state.current_q_idx + 1} 題**")
        
        st.info(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        st.markdown("<br>", unsafe_allow_html=True) # 增加間距

        if st.button("送出答案", key
