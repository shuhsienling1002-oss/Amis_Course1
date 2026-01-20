import streamlit as st
import time
import os
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 (行動優先設定) ---
st.set_page_config(
    page_title="阿美語小教室", 
    page_icon="🌞", 
    layout="centered", # 手機上置中顯示較佳
    initial_sidebar_state="collapsed"
)

# --- CSS 優化 (手機版面特化) ---
st.markdown("""
    <style>
    /* 1. 縮減手機頂部留白，爭取更多顯示空間 */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }
    
    /* 2. 按鈕樣式：更適合手指點擊的大按鈕 */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        background-color: #FFD700;
        color: #333;
        border: none;
        padding: 12px 0px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFC107;
        transform: translateY(-2px);
        box-shadow: 0px 6px 8px rgba(0,0,0,0.15);
    }
    .stButton>button:active {
        transform: translateY(1px);
    }

    /* 3. 卡片樣式：增加陰影與圓角，提升質感 */
    .card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 15px;
        border: 1px solid #eee;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* 4. 字體優化 */
    .big-font {
        font-size: 32px !important; /* 手機上稍微調小一點點以免換行 */
        font-weight: 800;
        color: #2E86C1;
        margin: 5px 0;
    }
    .med-font {
        font-size: 18px !important;
        color: #666;
        margin-bottom: 10px;
    }
    .emoji-icon {
        font-size: 50px;
        margin-bottom: 5px;
    }
    
    /* 5. 隱藏 Streamlit 預設漢堡選單與 Footer (選用，讓畫面更像 App) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. 數據結構 (Unit 1) ---
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "💆‍♂️", "action": "摸摸頭", "file": "Fongoh"},
    "Mata":     {"zh": "眼睛", "emoji": "👁️", "action": "眨眨眼", "file": "Mata"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "action": "指鼻子", "file": "Ngoso"}, 
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "action": "拉耳朵", "file": "Tangila"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "action": "張開嘴", "file": "Ngoyos"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "☺️", "action": "戳臉頰", "file": "Pising"}
}

SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？", "file": "q_what"},
    {"amis": "O {word} koni.", "zh": "這是{word}。", "file": "a_mata"}, 
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。", "file": None},
    {"amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。", "file": "cmd_dihdihen"}
]

# --- 1.5 智慧語音核心 ---
def play_audio(text, filename_base=None):
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
        tts = gTTS(text=text, lang='id') # 印尼語發音較接近
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (語音暫無法播放)")

# --- 2. 狀態管理 ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 ---

def show_learning_mode_u1():
    st.markdown("<div style='text-align: center; color: #888; margin-bottom: 10px;'>Unit 1: 我的身體</div>", unsafe_allow_html=True)
    st.info("👆 點擊播放按鈕聽發音！")
    
    # 手機版面優化：使用 columns 但 Streamlit 在手機會自動堆疊
    col1, col2 = st.columns(2)
    words = list(VOCABULARY.items())
    
    for idx, (amis, data) in enumerate(words):
        # 奇數偶數分配到不同欄位
        with (col1 if idx % 2 == 0 else col2):
            st.markdown(f"""
            <div class="card">
                <div class="emoji-icon">{data['emoji']}</div>
                <div class="big-font">{amis}</div>
                <div class="med-font">{data['zh']}</div>
                <div style="color: #999; font-size: 14px; border-top: 1px dashed #ddd; padding-top:5px;">
                    動作：{data['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(amis, filename_base=data.get('file'))

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    s1 = SENTENCES[0]
    s2 = SENTENCES[1] 
    
    # 句型卡片
    st.markdown(f"""
    <div class="card" style="background-color: #E8F8F5; border: none;">
        <div style="font-weight:bold; color:#16A085;">Q: {s1['amis']}</div>
        <div style="color:#555;">{s1['zh']}</div>
    </div>
    """, unsafe_allow_html=True)
    play_audio(s1['amis'], filename_base=s1.get('file'))
        
    st.markdown(f"""
    <div class="card" style="background-color: #FEF9E7; border: none;">
        <div style="font-weight:bold; color:#D4AC0D;">A: {s2['amis'].format(word='mata')}</div>
        <div style="color:#555;">這是眼睛。</div>
    </div>
    """, unsafe_allow_html=True)
    play_audio(s2['amis'].format(word='mata'), filename_base="a_mata") 

def show_quiz_mode_u1():
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🏆 小勇士挑戰</h3>", unsafe_allow_html=True)
    
    # 進度條
    st.progress(st.session_state.current_q / 3)
    st.write("") # Spacer

    if st.session_state.current_q == 0:
        # --- Q1 ---
        st.markdown("**第 1 關：聽聽看，這是誰？**")
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
                time.sleep(1.0)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("👁️ 眼睛"): st.error("不對喔！")

    elif st.session_state.current_q == 1:
        # --- Q2 ---
        st.markdown("**第 2 關：看圖回答**")
        st.markdown("他問：`O maan koni?` (這是什麼？)")
        play_audio("O maan koni?", filename_base="q_what")
        
        st.markdown("<div style='font-size:80px; text-align:center; margin: 20px 0;'>👄</div>", unsafe_allow_html=True)
        
        st.markdown("請完成句子： `O _______ koni.`")
        
        # 手機上 Radio 選項改為按鈕形式可能更好，但這裡先維持 Radio 比較清楚
        options = ["Fongoh (頭)", "Ngoyos (嘴巴)", "Pising (臉)"]
        choice = st.radio("請選擇：", options, label_visibility="collapsed")
        
        st.write("")
        if st.button("✅ 確定送出"):
            if "Ngoyos" in choice:
                st.success("太棒了！")
                play_audio("O Ngoyos koni", filename_base="a_ngoyos")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.error("再試一次！")

    elif st.session_state.current_q == 2:
        # --- Q3 ---
        st.markdown("**第 3 關：我是小隊長**")
        st.markdown("指令：`Dihdihen ko pising.`")
        play_audio("Dihdihen ko pising", filename_base="cmd_dihdihen")
        
        st.info("這是什麼動作？")
        
        if st.button("💆‍♂️ 摸摸頭"): st.error("那是 Fongoh 喔！")
        if st.button("☺️ 摸摸臉頰"):
            st.snow()
            st.success("完全正確！")
            time.sleep(1.5)
            st.session_state.score += 100
            st.session_state.current_q += 1
            st.rerun()

    else:
        # 結算畫面
        st.markdown(f"""
        <div class="card" style="background-color: #FFF8DC; border: 2px solid #FFD700;">
            <h1>🎉 挑戰完成！</h1>
            <h2 style="color: #E67E22;">得分：{st.session_state.score}</h2>
            <p>你真是太厲害了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 (單頁式架構) ---

# 標題區
st.title("阿美語小教室 🌞")

# 使用 Tabs 取代 Sidebar，更適合手機操作
tab1, tab2 = st.tabs(["📖 學習單詞", "🎮 練習挑戰"])

with tab1:
    show_learning_mode_u1()

with tab2:
    show_quiz_mode_u1()
