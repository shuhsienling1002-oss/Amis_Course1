import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# ==========================================
# 🔧 單元設定區 (請在此替換各單元的資料)
# ==========================================

UNIT_ID = "Unit 1"
UNIT_NAME = "O tireng no mako (我的身體)"
UNIT_ICON = "🙆‍♂️"

# 1. 單字資料庫
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "🙆‍♂️", "file": "Fongoh"},
    "Mata":     {"zh": "眼睛", "emoji": "👀", "file": "Mata"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "file": "Ngoso"}, 
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "file": "Tangila"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "file": "Ngoyos"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "😊", "file": "Pising"}
}

# 2. 句子資料庫
SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "q_what"},
    {"amis": "O mata koni.", "zh": "這是眼睛。", "file": "a_mata"}, 
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。", "file": None},
    {"amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。", "file": "cmd_dihdihen"}
]

# ==========================================
# 📱 系統核心 (以下程式碼 1-10 單元通用)
# ==========================================

st.set_page_config(
    page_title=f"{UNIT_ID}: {UNIT_NAME}", 
    page_icon=UNIT_ICON, 
    layout="centered",
    initial_sidebar_state="collapsed" # 手機版預設收起側邊欄
)

# --- CSS 手機版面優化 ---
st.markdown("""
    <style>
    /* 全域字體優化 */
    body { font-family: "Helvetica Neue", Arial, sans-serif; }
    
    /* 標題置中與調整 */
    h1, h2, h3 { text-align: center; color: #2C3E50; }
    
    /* 大按鈕樣式 (手機好點擊) */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        font-size: 20px;
        font-weight: bold;
        background-color: #FFD54F; /* 活潑黃 */
        color: #3E2723;
        border: none;
        padding: 12px 0px;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFCA28;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    
    /* 單字卡片樣式 */
    .word-card {
        background: linear-gradient(145deg, #ffffff, #f0f2f5);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 5px 5px 15px #d1d9e6, -5px -5px 15px #ffffff;
    }
    .emoji-icon { font-size: 50px; margin-bottom: 10px; }
    .amis-text { font-size: 28px; font-weight: bold; color: #1565C0; margin-bottom: 5px; }
    .zh-text { font-size: 18px; color: #546E7A; }
    
    /* 進度條顏色 */
    .stProgress > div > div > div > div { background-color: #42A5F5; }
    </style>
""", unsafe_allow_html=True)

# --- 語音播放模組 ---
def play_audio(text, filename_base=None):
    # 優先找 m4a (iOS錄音常見) -> mp3 -> Google TTS
    if filename_base:
        for ext in ['m4a', 'mp3']:
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                # 判斷 mime type
                mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                st.audio(path, format=mime)
                return

    # Fallback to gTTS
    try:
        tts = gTTS(text=text, lang='id') # 印尼語發音較接近
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (語音生成失敗)")

# --- 題目生成引擎 (核心邏輯) ---
def generate_quiz_questions():
    """隨機產生 3 題測驗，包含單字與句子"""
    questions = []
    
    # 將單字轉為列表以便隨機抽取
    vocab_keys = list(VOCABULARY.keys())
    
    # 題型 1: 聽音辨義 (單字)
    if len(vocab_keys) >= 3:
        target_word = random.choice(vocab_keys)
        # 建立選項：正確答案 + 2個隨機錯誤答案
        distractors = random.sample([k for k in vocab_keys if k != target_word], 2)
        options = [target_word] + distractors
        random.shuffle(options)
        
        questions.append({
            "type": "vocab_audio",
            "q_audio": target_word,
            "q_file": VOCABULARY[target_word].get('file'),
            "correct": VOCABULARY[target_word]['zh'], # 答案是中文意思
            # 選項顯示為中文，讓學生聽阿美語選中文
            "options": [VOCABULARY[opt]['zh'] for opt in options], 
            "hint": f"{target_word} 是 {VOCABULARY[target_word]['zh']}"
        })

    # 題型 2: 看圖/看中文 選阿美語 (單字)
    if len(vocab_keys) >= 3:
        target_word = random.choice(vocab_keys)
        distractors = random.sample([k for k in vocab_keys if k != target_word], 2)
        options = [target_word] + distractors
        random.shuffle(options)
        
        questions.append({
            "type": "vocab_visual",
            "q_text": f"{VOCABULARY[target_word]['emoji']} {VOCABULARY[target_word]['zh']}",
            "correct": target_word,
            "options": options,
            "hint": f"{VOCABULARY[target_word]['zh']} 的阿美語是 {target_word}"
        })

    # 題型 3: 句子理解 (若有句子)
    if len(SENTENCES) > 0:
        target_sent = random.choice(SENTENCES)
        # 簡單處理：如果是問答題，沒有自動產生的錯誤選項，這裡做簡化
        # 我們設計為：聽句子 -> 選擇正確的中文翻譯
        
        # 隨機抓取其他句子的中文當作干擾 (若不足則補假字)
        other_sentences = [s['zh'] for s in SENTENCES if s != target_sent]
        if len(other_sentences) < 2:
            distractors = ["(其他意思)", "(聽不懂)"] # 備用
        else:
            distractors = random.sample(other_sentences, min(2, len(other_sentences)))
            
        options = [target_sent['zh']] + distractors
        random.shuffle(options)
        
        questions.append({
            "type": "sentence_audio",
            "q_audio": target_sent['amis'],
            "q_file": target_sent.get('file'),
            "correct": target_sent['zh'],
            "options": options,
            "hint": f"{target_sent['amis']} 意思是 {target_sent['zh']}"
        })
    
    # 確保只有 3 題 (若上面產生不足 3 題則有多少用多少，通常會夠)
    return questions[:3]

# --- 狀態初始化 ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_data = generate_quiz_questions()
    st.session_state.init = True

# --- 頁面 1: 學習模式 ---
def show_learning_mode():
    st.markdown(f"## 📖 學習模式: {UNIT_ID}")
    
    tab1, tab2 = st.tabs(["🔤 單字卡", "🗣️ 句型練習"])
    
    with tab1:
        # 使用響應式網格
        cols = st.columns(2) # 手機上 Streamlit 會自動堆疊
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
            <div style="background-color:#E3F2FD; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 5px solid #2196F3;">
                <p style="font-size:20px; font-weight:bold; color:#1565C0; margin:0;">{sent['amis']}</p>
                <p style="color:#546E7A; margin:0;">{sent['zh']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"▶️ 播放句子 {i+1}", key=f"btn_sent_{i}"):
                play_audio(sent['amis'], sent.get('file'))

# --- 頁面 2: 測驗模式 ---
def show_quiz_mode():
    st.markdown(f"## 🎮 隨機挑戰: {UNIT_ID}")
    
    # 檢查題目是否已作答完畢
    if st.session_state.current_q_idx >= len(st.session_state.quiz_data):
        # 結算畫面
        st.markdown("""
        <div style='text-align: center; padding: 40px; background-color: #FFF3E0; border-radius: 20px;'>
            <h1 style='color: #FF9800;'>🎉 挑戰完成！</h1>
            <h2 style='color: #5D4037;'>得分：{} / {}</h2>
        </div>
        """.format(st.session_state.score, len(st.session_state.quiz_data) * 100), unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次 (重新抽題)"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_data = generate_quiz_questions() # 重新生成題目
            st.rerun()
        return

    # 顯示題目
    q_data = st.session_state.quiz_data[st.session_state.current_q_idx]
    
    # 進度條
    progress = (st.session_state.current_q_idx) / len(st.session_state.quiz_data)
    st.progress(progress)
    st.caption(f"第 {st.session_state.current_q_idx + 1} 題 / 共 {len(st.session_state.quiz_data)} 題")

    st.markdown("### ❓ 請回答：")
    
    # 根據題型顯示不同內容
    if q_data['type'] == 'vocab_audio':
        st.info("👂 請聽語音，選出正確的意思：")
        if st.button("🎧 播放聲音"):
            play_audio(q_data['q_audio'], q_data.get('q_file'))
            
    elif q_data['type'] == 'vocab_visual':
        st.info(f"👁️ 請問 **{q_data['q_text']}** 的阿美語是？")
        
    elif q_data['type'] == 'sentence_audio':
        st.info("👂 請聽句子，選出正確的意思：")
        if st.button("🎧 播放句子"):
            play_audio(q_data['q_audio'], q_data.get('q_file'))

    # 顯示選項 (使用 columns 讓按鈕在手機上更好看)
    # 這裡我們用一個簡單的 trick：用 radio 或 button 都可以，但 button 在手機上比較好按
    # 為了方便邏輯判斷，這裡示範用 st.radio 但用 CSS 優化過，或者直接用各個 button
    
    st.write("") # Spacer
    
    # 使用按鈕作為選項
    cols = st.columns(1) # 手機版單欄排列最清楚
    for opt in q_data['options']:
        if st.button(opt, key=f"opt_{st.session_state.current_q_idx}_{opt}"):
            if opt == q_data['correct']:
                st.balloons()
                st.success("✅ 答對了！")
                time.sleep(1)
                st.session_state.score += 100
            else:
                st.error(f"❌ 答錯了！正確答案是：{q_data['correct']}")
                time.sleep(2)
            
            # 前往下一題
            st.session_state.current_q_idx += 1
            st.rerun()

# --- 主程式切換 ---
mode = st.sidebar.radio("功能選單", ["📖 學習模式", "🎮 隨機測驗"])

if mode == "📖 學習模式":
    show_learning_mode()
else:
    show_quiz_mode()
