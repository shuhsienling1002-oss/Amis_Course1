import tkinter as tk
from tkinter import messagebox
import random

# ==========================================
# 🧠 Model Layer: 數據結構與內容 (The Knowledge Base)
# 符合 App-Lexicon-CRF v6.4 規範
# ==========================================
class CourseData:
    def __init__(self):
        #  嚴格校對蔡中涵辭典拼寫
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
        
        #  核心詞彙庫
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
        
        #  結構化句型
        self.sentences = [
            {"amis": "Ci Panay ko ngangan ako.", "zhtw": "我的名字是 Panay。"},
            {"amis": "Nani Makotaay kako.", "zhtw": "我來自 Makotaay。"},
            {"amis": "Maolah kako a romadiw.", "zhtw": "我喜歡唱歌。"},
            {"amis": "Maro' kako i Taypak.", "zhtw": "我住在台北。"},
            {"amis": "Lipahak kako a manengneng i tisowanan.", "zhtw": "很高興見到你。"}
        ]

# ==========================================
# 📱 View & Controller Layer: 介面與邏輯 (The App Engine)
# 符合 Code-CRF v6.4 (SRP 單一職責原則)
# ==========================================
class AmisLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Amis Master v1.0 - Intro Course")
        self.root.geometry("500x700")
        self.data = CourseData()
        
        # UI 配置 - 顏色符合阿美族傳統色 (紅/白/黑)
        self.bg_color = "#f0f0f0"
        self.primary_color = "#D32F2F" # Amis Red
        self.text_color = "#212121"
        self.root.configure(bg=self.bg_color)
        
        # 初始化 UI
        self.setup_home()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 1. 首頁 (Home) ---
    def setup_home(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Nga'ay ho!", font=("Helvetica", 24, "bold"), bg=self.bg_color, fg=self.primary_color).pack(pady=40)
        tk.Label(self.root, text="阿美語自我介紹課程", font=("Arial", 14), bg=self.bg_color).pack(pady=10)
        
        btn_style = {"font": ("Arial", 12), "width": 25, "height": 2, "bg": "white", "relief": "groove"}
        
        tk.Button(self.root, text="📖 閱讀文章 (Miasip)", command=self.show_article, **btn_style).pack(pady=10)
        tk.Button(self.root, text="🔑 學習單詞 (Tilid)", command=self.show_vocab, **btn_style).pack(pady=10)
        tk.Button(self.root, text="🗣️ 練習句型 (Sowal)", command=self.show_sentences, **btn_style).pack(pady=10)
        tk.Button(self.root, text="📝 隨堂測驗 (Test)", command=self.start_quiz, **btn_style, fg="red").pack(pady=10)

    # --- 2. 文章閱讀 (Article) ---
    def show_article(self):
        self.clear_screen()
        tk.Label(self.root, text=self.data.article["title"], font=("Helvetica", 18, "bold"), bg=self.bg_color, fg=self.primary_color).pack(pady=20)
        
        text_frame = tk.Frame(self.root, bg="white", padx=15, pady=15)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # [cite: 20] 視覺層級：留白與行距
        msg = tk.Message(text_frame, text=self.data.article["content"], font=("Georgia", 14), width=400, bg="white", justify="left")
        msg.pack()
        
        tk.Button(self.root, text="回首頁 (Back)", command=self.setup_home, bg="#DDDDDD").pack(pady=20)

    # --- 3. 單詞卡片 (Vocabulary) ---
    def show_vocab(self):
        self.clear_screen()
        tk.Label(self.root, text="核心單詞 (Vocabulary)", font=("Helvetica", 18, "bold"), bg=self.bg_color).pack(pady=20)
        
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(fill="both", expand=True, padx=20)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        canvas = tk.Canvas(list_frame, bg=self.bg_color, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas, bg=self.bg_color)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        for idx, word in enumerate(self.data.vocabulary):
            # [cite: 20] 拇指熱區與卡片式設計
            card = tk.Frame(inner_frame, bg="white", bd=1, relief="solid", padx=10, pady=10)
            card.pack(fill="x", pady=5, padx=5)
            tk.Label(card, text=f"{idx+1}. {word['amis']}", font=("Arial", 14, "bold"), bg="white", fg=self.primary_color).pack(side="left")
            tk.Label(card, text=f"({word['type']}) {word['zhtw']}", font=("Arial", 12), bg="white").pack(side="right")
        
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        tk.Button(self.root, text="回首頁", command=self.setup_home).pack(pady=10)

    # --- 4. 句型練習 (Sentences) ---
    def show_sentences(self):
        self.clear_screen()
        tk.Label(self.root, text="實戰句型 (Sentences)", font=("Helvetica", 18, "bold"), bg=self.bg_color).pack(pady=20)
        
        for sent in self.data.sentences:
            frame = tk.Frame(self.root, bg="white", pady=10, padx=10, relief="ridge", bd=2)
            frame.pack(fill="x", padx=20, pady=5)
            #  第一性原理：展示完整句構
            tk.Label(frame, text=sent['amis'], font=("Arial", 13, "bold"), bg="white", fg="#004D40").pack(anchor="w")
            tk.Label(frame, text=sent['zhtw'], font=("Arial", 11), bg="white", fg="gray").pack(anchor="w")
            
        tk.Button(self.root, text="回首頁", command=self.setup_home).pack(pady=20)

    # --- 5. 隨堂測驗 (Quiz) ---
    # [cite: 47] 遊戲化與回饋迴路
    def start_quiz(self):
        self.clear_screen()
        # 隨機抽取一題
        question = random.choice(self.data.vocabulary)
        self.current_q = question
        
        tk.Label(self.root, text="測驗：請問這個詞的意思？", font=("Arial", 14), bg=self.bg_color).pack(pady=30)
        tk.Label(self.root, text=question['amis'], font=("Arial", 28, "bold"), fg=self.primary_color, bg=self.bg_color).pack(pady=20)
        
        # 產生選項 (1個正確 + 2個錯誤)
        options = [question['zhtw']]
        while len(options) < 3:
            distractor = random.choice(self.data.vocabulary)['zhtw']
            if distractor not in options:
                options.append(distractor)
        random.shuffle(options)
        
        for opt in options:
            tk.Button(self.root, text=opt, font=("Arial", 14), width=20, 
                      command=lambda o=opt: self.check_answer(o)).pack(pady=10)
        
        tk.Button(self.root, text="放棄/回首頁", command=self.setup_home, bg="#DDDDDD").pack(pady=30)

    def check_answer(self, user_ans):
        #  即時回饋迴路
        if user_ans == self.current_q['zhtw']:
            messagebox.showinfo("Nga'ay!", "答對了！太棒了！ (Correct)")
            self.start_quiz() # 下一題
        else:
            messagebox.showerror("Aya...", f"答錯囉。\n正確答案是：{self.current_q['zhtw']}")

# ==========================================
# 🚀 System Boot
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AmisLearningApp(root)
    root.mainloop()
