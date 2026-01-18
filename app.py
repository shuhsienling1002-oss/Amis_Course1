import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(page_title="阿美語小教室", page_icon="🌞", layout="centered")

# CSS 優化 (卡片樣式、按鈕樣式)
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
        margin-top: 10px;
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
        margin-bottom: 0px;
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

# --- 1. 數據結構 (Unit 1) ---
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "🙆‍♂️", "action": "摸摸頭", "file": "Fongoh"},
    "Mata":     {"zh": "眼睛", "emoji": "👀", "action": "眨眨眼", "file": "Mata"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "action": "指鼻子", "file": "Ngoso"}, 
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "action": "拉耳朵", "file": "Tangila"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "action": "張開嘴", "file": "Ngoyos"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "😊", "action": "戳臉頰", "file": "Pising"}
}

SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "q_what"},
    {"amis": "O {word} koni.", "zh": "這是{word}。", "file": "a_mata"}, 
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。", "file": None},
    {"amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。", "file": "cmd_dihdihen"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
    """
    1. 優先尋找 audio/xxx.m4a (GitHub 上傳的手機錄音)
    2. 其次尋找 audio/xxx.mp3 (轉檔音訊)
    3. 如果都沒有，使用 Google TTS (印尼語代理)
    """
    
    if filename_base:
        # 檢查 m4a
        path_m4a = f"audio/{filename_base}.m4a"
        if os.path.exists(path_m4a):
            st.audio(path_m4a, format='audio/mp4')
            return
            
        # 檢查 mp3
        path_mp3 = f"audio/{filename_base}.mp3"
        if os.path.exists(path_mp3):
            st.audio(path_mp3, format='audio/mp3')
            return

    # 降級方案：Google TTS
    try:
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (無聲)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 (Unit 1 專用) ---

def show_learning_mode_u1():
    # 更新標題為 sakacecay
    st.markdown("<h2 style='text-align: center;'>sakacecay: O tireng no mako</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>我的身體</h4>", unsafe_allow_html=True)
    st.info("小朋友，現在是「真人老師」發音喔！點擊播放聽聽看！")
    
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
                
                # 呼叫智慧播放器
                play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    s2 = SENTENCES[1] 
    
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"Q: {s1['amis']}\n({s1['zh']})")
        play_audio(s1['amis'], filename_base=s1.get('file'))
        
    with c2:
        # 這裡保持小寫 mata
        display_text = s2['amis'].format(word='mata')
        st.warning(f"A: {display_text}\n(這是眼睛。)")
        play_audio(display_text, filename_base="a_mata") 

def show_quiz_mode_u1():
    # 更新標題為 sakacecay
    st.markdown("<h2 style='text-align: center;'>🎮 sakacecay 小勇士挑戰</h2>", unsafe_allow_html=True)
    progress = st.progress(st.session_state.current_q / 3)
    
    if st.session_state.current_q == 0:
        # --- Q1 ---
        st.markdown("### 第一關：聽聽看，這是誰？")
        st.write("請點擊播放：")
        
        target_word = "Tangila"
        play_audio(target_word, filename_base="Tangila")
        
        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👃 鼻子"): st.error("不對喔！")
        with c2:
            if st.button("👂 耳朵"):
                st.balloons()
                st.success("答對了！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("👀 眼睛"): st.error("不對喔！")

    elif st.session_state.current_q == 1:
        # --- Q2 ---
        st.markdown("### 第二關：看圖回答")
        st.markdown("#### 他問：「O maan koni?」")
        
        play_audio("O maan koni?", filename_base="q_what")
        
        col_img, col_opt = st.columns([1, 2])
        with col_img:
            st.markdown("<div style='font-size:80px; text-align:center;'>👄</div>", unsafe_allow_html=True)
        
        with col_opt:
            st.markdown("#### 請完成句子： O _______ koni.")
            options = ["Fongoh (頭)", "Ngoyos (嘴巴)", "Pising (臉)"]
            choice = st.radio("請選擇：", options)
            
            if st.button("確定送出"):
                if "Ngoyos" in choice:
                    st.success("太棒了！")
                    play_audio("O Ngoyos koni", filename_base="a_ngoyos")
                    time.sleep(2)
                    st.session_state.score += 100
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("再試一次！")

    elif st.session_state.current_q == 2:
        # --- Q3 ---
        st.markdown("### 第三關：我是小隊長")
        st.markdown("#### 指令： Dihdihen ko pising.")
        
        play_audio("Dihdihen ko pising", filename_base="cmd_dihdihen")
        
        st.info("請問這個指令是要你做什麼動作？")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🙆‍♂️ 摸摸頭"): st.error("那是 Fongoh 喔！")
        with c2:
            if st.button("😊 摸摸臉頰"):
                st.snow()
                st.success("完全正確！")
                time.sleep(2)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()

    else:
        st.markdown(f"""
        <div style='text-align: center; padding: 50px;'>
            <h1>🏆 挑戰完成！</h1>
            <h2>得分：{st.session_state.score}</h2>
        </div>
        """, unsafe_allow_html=True)
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
st.sidebar.title("阿美語小教室 🌞")

# 單元選擇器 (更新為 sakacecay)
unit_options = [
    "sakacecay: O tireng no mako (我的身體)",
    # "sakatusa: Oramod no mako (我的家人)",  # 未來可開啟
]
selected_unit = st.sidebar.selectbox("選擇單元", unit_options)

# 模式選擇
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

st.sidebar.markdown("---")
st.sidebar.caption(f"目前進度：{selected_unit}")

# 根據選擇的單元載入對應內容 (檢查字串中是否包含 sakacecay)
if "sakacecay" in selected_unit:
    if mode == "📖 學習單詞":
        show_learning_mode_u1()
    else:
        show_quiz_mode_u1()
else:
    # 未來單元的預留畫面
    st.markdown(f"## 🚧 {selected_unit}")
    st.info("這個單元正在努力建置中，敬請期待！")
