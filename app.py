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
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption("🔇 (語音無法播放)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 1: O Tireng", page_icon="🙆‍♂️", layout="centered")

# --- CSS 手機版面優化 ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
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
    .amis-text { font-size: 24px; font-weight: bold; color: #D84315; }
    .chinese-text { font-size: 18px; color: #7f8c8d; }
    .sentence-box {
        background-color: #FFEBEE;
        border-left: 5px solid #FF7043;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    .stButton>button {
        width: 100%; 
        border-radius: 12px; 
        font-size: 20px; 
        font-weight: 600;
        background-color: #FFCCBC; 
        color: #BF360C; 
        border: 2px solid #D84315; 
        padding: 12px;
        margin-top: 10px;
    }
    .stButton>button:hover { background-color: #FFAB91; border-color: #BF360C; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 ---
vocab_data = [
    {"amis": "Fongoh", "chi": "頭", "icon": "🙆‍♂️"},
    {"amis": "Mata", "chi": "眼睛", "icon": "👀"},
    {"amis": "Ngoso'", "chi": "鼻子", "icon": "👃"},
    {"amis": "Tangila", "chi": "耳朵", "icon": "👂"},
    {"amis": "Ngoyos", "chi": "嘴巴", "icon": "👄"},
    {"amis": "Pising", "chi": "臉 / 臉頰", "icon": "😊"}
]

sentences = [
    {"amis": "O maan koni?", "chi": "這是什麼？", "icon": "❓"},
    {"amis": "O mata koni.", "chi": "這是眼睛。", "icon": "👀"},
    {"amis": "Piti'en ko mata.", "chi": "閉上眼睛。", "icon": "😌"},
    {"amis": "Dihdihen ko pising.", "chi": "摸摸臉頰。", "icon": "👉"}
]

# 題庫池
raw_quiz_pool = [
    {"q": "單字測驗：Mata", "audio": "Mata", "options": ["眼睛", "鼻子", "耳朵"], "ans": "眼睛"},
    {"q": "單字測驗：Ngoso'", "audio": "Ngoso'", "options": ["鼻子", "嘴巴", "頭"], "ans": "鼻子"},
    {"q": "單字測驗：Tangila", "audio": "Tangila", "options": ["耳朵", "臉", "眼睛"], "ans": "耳朵"},
    {"q": "單字測驗：Ngoyos", "audio": "Ngoyos", "options": ["嘴巴", "頭", "鼻子"], "ans": "嘴巴"},
    {"q": "單字測驗：Fongoh", "audio": "Fongoh", "options": ["頭", "臉", "耳朵"], "ans": "頭"},
    {"q": "單字測驗：Pising", "audio": "Pising", "options": ["臉 / 臉頰", "嘴巴", "眼睛"], "ans": "臉 / 臉頰"},
    {"q": "句子聽力：Piti'en ko mata.", "audio": "Piti'en ko mata", "options": ["閉上眼睛", "摸摸臉", "這是什麼"], "ans": "閉上眼睛"}
]

# --- 3. 狀態初始化 (一次抽 3 題) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 隨機抽 3 題
    selected_questions = random.sample(raw_quiz_pool, 3)
    for q in selected_questions:
        random.shuffle(q['options']) # 洗牌選項
    st.session_state.quiz_questions = selected_questions
    st.session_state.init = True

# --- 4. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #D84315;'>Unit 1: O Tireng</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 學習詞彙", "🎲 隨機挑戰"])

with tab1:
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""<div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"🔊", key=f"v_{i}"):
                safe_play_audio(word['amis'])
    
    st.markdown("---")
    for i, s in enumerate(sentences):
        st.markdown(f"""<div class="sentence-box">
            <div style="font-size: 18px; font-weight: bold; color: #D84315;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555;">{s['chi']}</div>
        </div>""", unsafe_allow_html=True)
        if st.button(f"▶️ 播放", key=f"s_{i}"):
            safe_play_audio(s['amis'])

with tab2:
    st.subheader("🎲 隨機評量 (共3題)")
    
    if st.session_state.current_q_idx < 3:
        q_idx = st.session_state.current_q_idx
        q_data = st.session_state.quiz_questions[q_idx]
        
        st.progress((q_idx) / 3)
        st.write(f"### 第 {q_idx + 1} 題")
        st.info(q_data['q'])
        
        if st.button("🎧 播放音檔", key=f"audio_{q_idx}"):
            safe_play_audio(q_data['audio'])
            
        # 選項
        user_choice = st.radio("選擇正確答案：", q_data['options'], key=f"choice_{st.session_state.quiz_id}_{q_idx}")
        
        if st.button("送出答案", key=f"submit_{q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("✅ 答對了！")
                time.sleep(1)
            else:
                st.error(f"❌ 答錯了！正確答案是：{q_data['ans']}")
                time.sleep(2)
            
            st.session_state.current_q_idx += 1
            safe_rerun()
    else:
        st.balloons()
        st.success("🏆 恭喜完成測試！")
        if st.button("🔄 重新挑戰 (隨機換題)"):
            del st.session_state.init # 強制觸發重新初始化
            safe_rerun()
