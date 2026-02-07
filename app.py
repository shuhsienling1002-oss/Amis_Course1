import streamlit as st
import random
import time

# ==========================================
# 🧠 Model Layer: 數據結構與內容 (The Knowledge Base)
# 符合 App-Lexicon-CRF v6.4 規範 - 嚴格鎖定蔡中涵辭典拼寫 [cite: 36]
# ==========================================
class CourseData:
    def __init__(self):
        self.article = {
            "title": "Ci Panay Kako (我是 Panay)",
            "content": """Nga'ay ho, salikaka mapolong.
Ci Panay ko ngangan ako. Nani Makotaay a niyaro' kako.
O Amis kako. Anini, maro' kako i Taypak, o matayalay kako i kosi.
Maolah kako a miasip to cudad, maolah haca a romadiw to radiw no Amis.
I demak no paratoh, tayra kako i riyar a mifoting.
Adihay ko widang ako i Taypak.
Lipahak kako a manengneng i tamowanan.
Nanay mapalipahak kita mapolong anini a romi'ad.
Aray, kansya."""
        }
        
        # 核心詞彙庫 
        self.vocabulary = [
            {"amis": "Ngangan", "zhtw": "名字", "type": "N"},
            {"amis": "Niyaro'", "zhtw": "部落/村莊", "type": "N"},
            {"amis": "Amis", "zhtw": "阿美族", "type": "N"},
            {"amis": "Maro'", "zhtw": "居住/坐", "type": "V"},
            {"amis": "Matayalay", "zhtw": "工作者", "type": "N"},
            {"amis": "Maolah", "zhtw": "喜歡", "type": "V"},
            {"amis": "Romadiw", "zhtw": "唱歌", "type": "V"},
            {"amis": "Riyar", "zhtw": "海洋", "type": "N"},
            {"amis": "Widang", "zhtw": "朋友", "type": "N"},
            {"amis": "Lipahak", "zhtw": "快樂", "type": "Adj"}
        ]
        
        # 結構化句型 - 第一性原理 VSO 結構 [cite: 46]
        self.sentences = [
            {"amis": "Ci Panay ko ngangan ako.", "zhtw": "我的名字是 Panay。", "note": "名詞句結構"},
            {"amis": "Nani Makotaay kako.", "zhtw": "我來自 Makotaay。", "note": "來源結構"},
            {"amis": "Maolah kako a romadiw.", "zhtw": "我喜歡唱歌。", "note": "喜好表達"},
            {"amis": "Maro' kako i Taypak.", "zhtw": "我住在台北。", "note": "位置標記 (i)"},
            {"amis": "Lipahak kako a manengneng i tisowanan.", "zhtw": "很高興見到你。", "note": "情感表達"}
        ]

# ==========================================
# 📱 View & Controller Layer: Streamlit 介面邏輯
# 符合 Ops-AI-CRF v6.4 (Headless Solutions) 
# ==========================================
def main():
    # 設置頁面配置
    st.set_page_config(page_title="Amis Master - Intro Course", page_icon="🎓")
    
    # 初始化數據
    data = CourseData()

    # 側邊欄導航 (Navigation)
    st.sidebar.title("Amis Master v1.0")
    choice = st.sidebar.radio("課程單元 (Unit)", ["🏠 首頁 (Home)", "📖 閱讀文章 (Miasip)", "🔑 核心單詞 (Tilid)", "🗣️ 實戰句型 (Sowal)", "📝 隨堂測驗 (Test)"])

    # --- 1. 首頁 (Home) ---
    if choice == "🏠 首頁 (Home)":
        st.title("Nga'ay ho! 👋")
        st.subheader("阿美語自我介紹課程 (Self-Introduction)")
        st.write("歡迎來到 Amis Master。本課程將帶領您學會如何用標準的阿美語介紹自己。")
        st.info("請使用左側選單切換學習模式。")
        
        # EdTech-CRF: 學習動機激勵 [cite: 47]
        st.markdown("### 🎯 學習目標")
        st.markdown("- 學會 **10** 個高頻單字")
        st.markdown("- 掌握 **5** 個 VSO 句型")
        st.markdown("- 能流暢閱讀 **100** 字短文")

    # --- 2. 文章閱讀 (Article) ---
    elif choice == "📖 閱讀文章 (Miasip)":
        st.header(data.article["title"])
        st.markdown("---")
        # 使用區塊引言顯示文章
        st.markdown(f"> {data.article['content'].replace(chr(10), '  '+chr(10))}")
        st.caption("試著大聲朗讀看看！(Try to read it aloud!)")

    # --- 3. 核心單詞 (Vocabulary) ---
    elif choice == "🔑 核心單詞 (Tilid)":
        st.header("核心單詞 (Vocabulary)")
        
        # 使用 Streamlit 的列佈局 (Columns) 呈現卡片效果
        for word in data.vocabulary:
            with st.expander(f"**{word['amis']}** ({word['type']})"):
                st.markdown(f"### {word['zhtw']}")
                st.caption("請注意重音與喉塞音 (') 的發音。")

    # --- 4. 實戰句型 (Sentences) ---
    elif choice == "🗣️ 實戰句型 (Sowal)":
        st.header("實戰句型 (Sentences)")
        st.write("掌握 VSO (動詞在前) 的語序邏輯：")
        
        for i, sent in enumerate(data.sentences):
            st.markdown(f"#### {i+1}. {sent['amis']}")
            st.text(f"中文：{sent['zhtw']}")
            st.caption(f"💡 解析：{sent['note']}")
            st.divider()

    # --- 5. 隨堂測驗 (Quiz) ---
    elif choice == "📝 隨堂測驗 (Test)":
        st.header("隨堂測驗 (Quiz)")
        
        # 使用 Session State 管理測驗狀態 (防止刷新後重置) [cite: 47]
        if 'quiz_q' not in st.session_state:
            st.session_state.quiz_q = None
            st.session_state.quiz_opts = []

        # 產生新題目按鈕
        if st.button("🔄 開始出題 / 下一題 (Next Question)"):
            q = random.choice(data.vocabulary)
            st.session_state.quiz_q = q
            
            # 產生選項
            options = [q['zhtw']]
            while len(options) < 3:
                distractor = random.choice(data.vocabulary)['zhtw']
                if distractor not in options:
                    options.append(distractor)
            random.shuffle(options)
            st.session_state.quiz_opts = options
            # 清除之前的回答記錄
            if 'last_answer' in st.session_state:
                del st.session_state.last_answer

        # 顯示題目
        if st.session_state.quiz_q:
            q = st.session_state.quiz_q
            st.markdown(f"### 請問 **{q['amis']}** 的意思是？")
            
            # 顯示選項
            with st.form("quiz_form"):
                answer = st.radio("請選擇答案：", st.session_state.quiz_opts)
                submitted = st.form_submit_button("送出答案 (Submit)")
                
                if submitted:
                    if answer == q['zhtw']:
                        st.success("🎉 Nga'ay! 答對了！(Correct)")
                        st.balloons()
                    else:
                        st.error(f"❌ Aya... 答錯了。正確答案是：{q['zhtw']}")

if __name__ == "__main__":
    main()
