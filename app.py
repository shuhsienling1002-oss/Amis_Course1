import streamlit as st
import requests # 新增
from streamlit_lottie import st_lottie # 新增
# ... (其他 import 保持不變)

# ==========================================
# 3.5 動態視覺層 (Motion Layer) - 新增模組
# ==========================================

class LottieEngine:
    """負責加載與渲染 Lottie 動畫"""
    
    @staticmethod
    @st.cache_data(show_spinner=False)
    def load_url(url):
        """從網路加載 JSON 動畫檔 (有緩存機制)"""
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    @staticmethod
    def render(url, height=150, key=None):
        """渲染動畫組件"""
        lottie_json = LottieEngine.load_url(url)
        if lottie_json:
            st_lottie(lottie_json, height=height, key=key)
        else:
            # 如果加載失敗，顯示一個靜態 Emoji 作為備案 (降級策略)
            st.markdown(f"<div style='font-size:{height/2}px; text-align:center;'>🤖</div>", unsafe_allow_html=True)

# --- 定義一些免費的動畫資源 (來自 LottieFiles) ---
ANIMATIONS = {
    # 一個可愛的搖頭/眨眼動畫，代替原本的靜態 Emoji
    "head_moving": "https://lottie.host/5a092822-13f5-47f6-a7f4-279549495147/o3Xz7y2g3P.json", 
    # 答對時的慶祝動畫
    "success": "https://lottie.host/81729a4d-0839-4467-8438-232537901726/H2a6j9q9k9.json"
}

# ==========================================
# 修改後的渲染邏輯 (以 render_learning_mode 為例)
# ==========================================

def render_learning_mode():
    st.markdown("### 📚 Unit 1: 我的身體")
    
    # --- 示範：將第一個單詞 'Fongoh' 升級為動態版 ---
    
    # 1. 顯示動態卡片 (Fongoh)
    st.markdown("""
    <div class="learn-card">
        <div class="card-header">
            <div>
                <div class="card-title">Fongoh</div>
                <div class="card-sub">頭</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 在卡片內部或下方放入動畫
    col_anim, col_btn = st.columns([2, 1])
    with col_anim:
        # 這裡呼叫 Lottie 引擎！
        LottieEngine.render(ANIMATIONS["head_moving"], height=120, key="anim_fongoh")
    with col_btn:
        # 垂直置中按鈕 (透過 CSS 或簡單的 padding)
        st.write("") 
        st.write("")
        if st.button("🔊", key="btn_anim_fongoh"):
            AudioManager.play("Fongoh")
            
    st.markdown("---")
    
    # 2. 其他單詞維持靜態 (混合模式，節省資源)
    # ... (原本的迴圈代碼可以放在這裡)

# ==========================================
# 修改後的測驗邏輯 (加入慶祝動畫)
# ==========================================
# 在 QuizEngine.next_step 中加入：

    # ... (在 st.balloons() 之後)
    with st.columns([1,2,1])[1]: # 置中顯示
        LottieEngine.render(ANIMATIONS["success"], height=200, key=f"win_{time.time()}")
    time.sleep(2) # 讓用戶看完動畫
    # ...
