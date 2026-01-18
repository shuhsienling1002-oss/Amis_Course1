import streamlit as st
import time
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置與 CSS 優化 (Layer 0: Pre-processing) ---
st.set_page_config(
    page_title="阿美語小教室", 
    page_icon="🌞", 
    layout="centered"
)

# 注入自定義 CSS 以適應低年級學童 (大字體、圓角、鮮豔色彩)
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
    .instruction {
        font-size: 20px;
        color: #444;
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 物理邏輯內核 (Layer 1: Data Structure) ---

# 詞彙庫 (已修正：Ngoyos, Pising)
VOCABULARY = {
    "Fongoh":   {"zh": "頭", "emoji": "🙆‍♂️", "action": "摸摸頭"},
    "Mata":     {"zh": "眼睛", "emoji": "👀", "action": "眨眨眼"},
    "Ngoso'":   {"zh": "鼻子", "emoji": "👃", "action": "指鼻子"},
    "Tangila":  {"zh": "耳朵", "emoji": "👂", "action": "拉耳朵"},
    "Ngoyos":   {"zh": "嘴巴", "emoji": "👄", "action": "張開嘴"},
    "Pising":   {"zh": "臉頰/臉", "emoji": "😊", "action": "戳臉頰"}
}

# 句型庫 (已修正：Dihdihen)
SENTENCES = [
    {"amis": "O maan koni?", "zh": "這是什麼？"},
    {"amis": "O {word} koni.", "zh": "這是{word}。"},
    {"amis": "Piti'en ko mata.", "zh": "閉上眼睛。"},
    {"amis": "Dihdihen ko pising.", "zh": "摸摸臉頰。"}
]

# --- 1.5 語音合成模組 (Layer 1.5: Audio Proxy) ---
@st.cache_data(show_spinner=False)
def get_audio_bytes(text):
    """
    使用 Google TTS (印尼語代理) 生成阿美語發音。
    使用 @st.cache_data 避免重複請求 Google API，加快載入速度。
    """
    try:
        # lang='id' (Indonesian) 是南島語系發音的最佳替代方案
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        return None

# --- 2. 狀態管理 (Session State) ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0

# --- 3. 介面邏輯 (UI Logic) ---

def show_learning_mode():
    st.markdown("<h1 style='text-align: center;'>🌞 阿美語身體歌 🌞</h1>", unsafe_allow_html=True)
    st.info("小朋友，點擊播放按鈕聽聽看，然後跟著做動作喔！")
    
    # 使用 2x3 網格展示單詞
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
                
                # 語音播放器
                audio_data = get_audio_bytes(amis)
                if audio_data:
                    st.audio(audio_data, format='audio/mp3', start_time=0)
                else:
                    st.caption("⚠️ 無法載入語音")

    st.markdown("---")
    st.markdown("### 🗣️ 句型練習")
    
    # 句型展示與語音
    s1 = SENTENCES[0]['amis']
    s2 = SENTENCES[1]['amis'].format(word='Mata')
    
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"Q: {s1}\n({SENTENCES[0]['zh']})")
        audio_s1 = get_audio_bytes(s1)
        if audio_s1: st.audio(audio_s1, format='audio/mp3')
        
    with c2:
        st.warning(f"A: {s2}\n(這是眼睛。)")
        audio_s2 = get_audio_bytes(s2)
        if audio_s2: st.audio(audio_s2, format='audio/mp3')

def show_quiz_mode():
    st.markdown("<h1 style='text-align: center;'>🎮 小勇士挑戰 🎮</h1>", unsafe_allow_html=True)
    
    # 進度條
    progress = st.progress(st.session_state.current_q / 3)
    
    # 題目邏輯
    if st.session_state.current_q == 0:
        # --- 題目 1: 聽音辨位 ---
        st.markdown("### 第一關：聽聽看，這是誰？")
        st.markdown("<div class='instruction'>請點擊下面的播放按鈕，然後選出正確的圖片！</div>", unsafe_allow_html=True)
        
        # 播放題目語音
        target_word = "Tangila"
        audio_q1 = get_audio_bytes(target_word)
        if audio_q1:
            st.audio(audio_q1, format='audio/mp3')
        
        st.write("") # 空行
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("👃 鼻子"):
                st.error("不對喔，那是 Ngoso'！")
        with c2:
            if st.button("👂 耳朵"):
                st.balloons()
                st.success(f"答對了！{target_word} 是耳朵！")
                time.sleep(1.5)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()
        with c3:
            if st.button("👀 眼睛"):
                st.error("不對喔，那是 Mata！")

    elif st.session_state.current_q == 1:
        # --- 題目 2: 句型重組 ---
        st.markdown("### 第二關：看圖回答")
        st.markdown("#### 他問：「O maan koni?」(這是什麼？)")
        
        # [新增] 播放問題語音
        q2_audio = get_audio_bytes("O maan koni")
        if q2_audio: st.audio(q2_audio, format='audio/mp3')
        
        col_img, col_opt = st.columns([1, 2])
        with col_img:
            # 顯示嘴巴圖示
            st.markdown("<div style='font-size:80px; text-align:center;'>👄</div>", unsafe_allow_html=True)
        
        with col_opt:
            st.markdown("#### 請完成句子： O _______ koni.")
            options = ["Fongoh (頭)", "Ngoyos (嘴巴)", "Pising (臉)"]
            choice = st.radio("請選擇正確的單詞：", options)
            
            if st.button("確定送出"):
                if "Ngoyos" in choice:
                    st.success("太棒了！ O Ngoyos koni.")
                    # 播放正確答案語音
                    ans_audio = get_audio_bytes("O Ngoyos koni")
                    if ans_audio: st.audio(ans_audio, format='audio/mp3', autoplay=True)
                    
                    time.sleep(2)
                    st.session_state.score += 100
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("再看仔細一點喔！圖片是嘴巴。")

    elif st.session_state.current_q == 2:
        # --- 題目 3: 動作指令 (已修正 Dihdihen) ---
        st.markdown("### 第三關：我是小隊長")
        
        command_text = "Dihdihen ko pising"
        st.markdown(f"#### 指令： {command_text}.")
        
        # 播放指令語音
        audio_q3 = get_audio_bytes(command_text)
        if audio_q3: st.audio(audio_q3, format='audio/mp3')
        
        st.info("請問這個指令是要你做什麼動作？")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🙆‍♂️ 摸摸頭"):
                st.error("那是 Fongoh 喔！")
        with c2:
            if st.button("😊 摸摸臉頰"):
                st.snow()
                st.success("完全正確！Pising 是臉頰，Dihdihen 是摸摸！")
                time.sleep(2)
                st.session_state.score += 100
                st.session_state.current_q += 1
                st.rerun()

    else:
        # --- 結算畫面 ---
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background-color: #fff; border-radius: 20px;'>
            <h1>🏆 挑戰完成！ 🏆</h1>
            <h2 style='color: #FFD700;'>你的得分：{st.session_state.score} 分</h2>
            <p style='font-size: 20px;'>你是阿美語小天才！Ma'orad to! (下雨般的掌聲/太棒了)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("再玩一次"):
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.rerun()

# --- 4. 主程式入口 ---
st.sidebar.title("導航列")
mode = st.sidebar.radio("選擇模式", ["📖 學習單詞", "🎮 練習挑戰"])

st.sidebar.markdown("---")
st.sidebar.info("💡 提示：點擊播放按鈕可以聽到阿美語發音喔！")

if mode == "📖 學習單詞":
    show_learning_mode()
else:
    show_quiz_mode()

st.sidebar.caption("Designed for Grade 1-2 Amis Learning")
