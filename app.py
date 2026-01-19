import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# ==========================================
# 🔧 單元設定區 (Unit 1 專屬資料)
# ==========================================

UNIT_ID = "Unit 1"
UNIT_NAME = "O tireng no mako (我的身體)"
UNIT_ICON = "🙆‍♂️"

# 1. 單字資料庫
# 格式：Amis: {中文, Emoji, 錄音檔名}
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "🙆‍♂️", "file": "Fongoh"},
    "Mata":     {"zh": "眼睛", "emoji": "👀", "file": "Mata"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "file": "Ngoso"}, 
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "file": "Tangila"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "file": "Ngoyos"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "😊", "file": "Pising"}
}

# 2. 句子資料庫
# 格式：{阿美語, 中文翻譯, 錄音檔名}
SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "q_what"},
    {"amis": "O mata koni.", "zh": "這是眼睛。", "file": "a_mata"}, 
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。", "file": None},
    {"amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。", "file": "cmd_dihdihen"}
]

# ==========================================
# 📱 系統核心 (UI與邏輯)
# ==========================================

st.set_page_config(
    page_title=f"{UNIT_ID}: {UNIT_NAME}", 
    page_icon=UNIT_ICON, 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS 手機版面優化 ---
st.markdown("""
    <style>
    /* 全域字體優化 */
    body { font-family: "Helvetica Neue", Arial, sans-serif; }
    
    /* 標題置中 */
    h1, h2, h3 { text-align: center; color: #2C3E50; }
    
    /* 大按鈕樣式 (手機好點擊) */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        font-size: 22px; /* 字體加大 */
        font-weight: bold;
        background-color: #FFD54F; /* 活潑黃 */
        color: #3E2723;
        border: none;
        padding: 15px 0px; /* 增加高度 */
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #FFCA28;
        transform: translateY(-2px);
    }
    
    /* 單字卡片樣式 */
    .word-card {
        background: linear-gradient(145deg, #ffffff, #f0f2f5);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.05);
    }
    .emoji-icon { font-size: 55px; margin-bottom: 5px; }
    .amis-text { font-size: 26px; font-weight: bold; color: #1565C0; margin-bottom: 0px; }
    .zh-text { font-size: 18px; color: #546E7A; }
    
    /* 句子框樣式 */
    .sentence-box {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #2196F3;
    }
    </style>
""", unsafe_allow_html=True)

# --- 語音播放模組 (支援 m4a/mp3/TTS) ---
def play_audio(text, filename_base=None):
    if filename_base:
        # 優先搜尋預錄好的音檔
        for ext in ['m4a', 'mp3']:
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                st.audio(path, format=mime)
                return

    # 若無音檔，使用 Google TTS (印尼語口音近似)
    try:
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (語音生成失敗)")

# --- 題目生成引擎 (隨機出題邏輯) ---
def generate_quiz_questions():
    """從單字和句子中隨機產生 3 題"""
    questions = []
    vocab_keys = list(VOCABULARY.keys())
    
    # 1. 確保有足夠單字
    if len(vocab_keys) < 3:
        return []

    # 題型 A: 聽單字 -> 選中文 (1題)
    target_word = random.choice(vocab_keys)
    distractors = random.sample([k for k in vocab_keys if k != target_word], 2)
    options = [target_word] + distractors
    random.shuffle(options)
    
    questions.append({
        "type": "vocab_audio",
        "question": "👂 請聽語音，選出正確的意思：",
        "audio_text": target_word,
        "audio_file": VOCABULARY[target_word].get('file'),
        "correct_answer": VOCABULARY[target_word]['zh'],
        "options": [VOCABULARY[opt]['zh'] for opt in options], # 選項顯示中文
        "hint": f"{target_word} 是 {VOCABULARY[target_word]['zh']}"
    })

    # 題型 B: 看中文/圖 -> 選阿美語 (1題)
    target_word_2 = random.choice([k for k in vocab_keys if k != target_word]) # 避免重複
    distractors_2 = random.sample([k for k in vocab_keys if k != target_word_2], 2)
    options_2 = [target_word_2] + distractors_2
    random.shuffle(options_2)

    questions.append({
        "type": "vocab_visual",
        "question": f"👁️ 請問 **{VOCABULARY[target_word_2]['emoji']} {VOCABULARY[target_word_2]['zh']}** 的阿美語是？",
        "correct_answer": target_word_2,
        "options": options_2, # 選項顯示阿美語
        "hint": f"{VOCABULARY[target_word_2]['zh']} 是 {target_word_2}"
    })

    # 題型 C: 聽句子 -> 選中文 (1題)
    if SENTENCES:
        target_sent = random.choice(SENTENCES)
        # 產生錯誤選項：隨機抓其他句子的中文，若不夠則補假選項
        other_sents_zh = [s['zh'] for s in SENTENCES if s != target_sent]
        if len(other_sents_zh) >= 2:
            distractors_sent = random.sample(other_sents_zh, 2)
        else:
            distractors_sent = ["(其他意思)", "(聽不懂)"]
            
        options_sent = [target_sent['zh']] + distractors_sent
        random.shuffle(options_sent)

        questions.append({
            "type": "sentence_audio",
            "question": "👂 請聽句子，選出正確的意思：",
            "audio_text": target_sent['amis'],
            "audio_file": target_sent.get('file'),
            "correct_answer": target_sent['zh'],
            "options": options_sent,
            "hint": f"{target_sent['amis']} \n 意思是：{target_sent['zh']}"
        })
    
    return questions

# --- 初始化 Session State ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_data = generate_quiz_questions()
    st.session_state.init = True

# --- 頁面 1: 學習模式 ---
def show_learning_mode():
    st.markdown(f"## 📖 學習: {UNIT_NAME}")
    
    tab1, tab2 = st.tabs(["🔤 核心單字", "🗣️ 實用句型"])
    
    with tab1:
        # 手機版面：使用 columns(2) 會自動在小螢幕變成直排，但在平板會並排
        cols = st.columns(2)
        for i, (amis, data) in enumerate(VOCABULARY.items()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="word-card">
                    <div class="emoji-icon">{data['emoji']}</div>
                    <div class="amis-text">{amis}</div>
                    <div class="zh-text">{data['zh']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🔊 播放", key=f"btn_vocab_{i}"):
                    play_audio(amis, data.get('file'))

    with tab2:
        for i, sent in enumerate(SENTENCES):
            st.markdown(f"""
            <div class="sentence-box">
                <p style="font-size:22px; font-weight:bold; color:#1565C0; margin:0;">{sent['amis']}</p>
                <p style="color:#546E7A; margin:5px 0 0 0; font-size:18px;">{sent['zh']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶️ 播放句子 {i+1}", key=f"btn_sent_{i}"):
                play_audio(sent['amis'], sent.get('file'))

# --- 頁面 2: 測驗模式 ---
def show_quiz_mode():
    st.markdown(f"## 🎮 隨機挑戰 (共3題)")
    
    # 檢查是否完成所有題目
    if st.session_state.current_q_idx >= len(st.session_state.quiz_data):
        st.markdown(f"""
        <div style='text-align: center; padding: 40px; background-color: #E8F5E9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #2E7D32;'>🎉 挑戰完成！</h1>
            <h2 style='color: #1B5E20;'>得分：{st.session_state.score} / {len(st.session_state.quiz_data) * 100}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次 (重新抽題)"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_data = generate_quiz_questions()
            st.rerun()
        return

    # 取得當前題目
    q_data = st.session_state.quiz_data[st.session_state.current_q_idx]
    
    # 顯示進度
    progress = (st.session_state.current_q_idx + 1) / len(st.session_state.quiz_data)
    st.progress(progress)
    st.caption(f"第 {st.session_state.current_q_idx + 1} 題")

    # 顯示題目內容
    st.info(q_data['question'])
    
    # 如果有音檔或語音
    if 'audio_text' in q_data:
        if st.button("🎧 播放聲音 (點擊收聽)", key=f"play_q_{st.session_state.current_q_idx}"):
            play_audio(q_data['audio_text'], q_data.get('audio_file'))

    st.write("") # 空行間距

    # 顯示選項 (手機版直排)
    for opt in q_data['options']:
        # 使用 callback 處理點擊，避免邏輯複雜
        def check_answer(selected_opt=opt):
            if selected_opt == q_data['correct_answer']:
                st.session_state.score += 100
                st.balloons()
                st.success("✅ 答對了！")
            else:
                st.error(f"❌ 答錯了！\n\n提示：{q_data['hint']}")
            
            time.sleep(1.5) # 讓使用者看到結果
            st.session_state.current_q_idx += 1
            
        st.button(opt, on_click=check_answer, key=f"opt_{st.session_state.current_q_idx}_{opt}")

# --- 主程式切換 ---
mode = st.sidebar.radio("功能選單", ["📖 學習模式", "🎮 隨機測驗"])

if mode == "📖 學習模式":
    show_learning_mode()
else:
    show_quiz_mode()
