[ruaydee.py](https://github.com/user-attachments/files/29807052/ruaydee.py)
import os
import random
import pandas as pd
import streamlit as st

# ==========================================
# 1. ตั้งค่าหน้าเว็บธีมสำนักพยากรณ์ RUAYDEE (Mystic Cool Theme)
# ==========================================
st.set_page_config(
    page_title="RUAYDEE - สำนักพยากรณ์เลขนำโชค 🔮", 
    page_icon="💰", 
    layout="centered"
)

# ตกแต่ง CSS โทนสีเย็นลึกลับ (น้ำเงินเข้ม, ฟ้าคราม, ม่วงนีออน) สไตล์ RUAYDEE
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
    
    * {
        font-family: 'Kanit', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    .fortune-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 2px solid #38bdf8;
        text-align: center;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    .fortune-title {
        color: #38bdf8;
        font-size: 36px;
        font-weight: 600;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.6);
        letter-spacing: 2px;
    }
    .mascot-box {
        background: rgba(15, 23, 42, 0.6);
        border-left: 5px solid #a855f7;
        border-radius: 12px;
        padding: 15px;
        font-size: 16px;
        color: #e2e8f0;
        margin: 20px 0;
        text-align: left;
    }
    .lucky-number-display {
        font-size: 72px;
        font-weight: bold;
        color: #4ade80;
        text-shadow: 0 0 20px rgba(74, 222, 128, 0.6);
        letter-spacing: 5px;
        margin: 15px 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. ระบบค้นหาและโหลดไฟล์อัจฉริยะ (Smart Loader)
# ==========================================
@st.cache_data
def load_lotto_data():
    # รายชื่อชื่อไฟล์ที่เป็นไปได้ทั้งหมดในเครื่องคุณ
    possible_files = [
        "to_lotto_2.xlsx",
        "to_lotto.xlsx",
        "to_lotto.csv"
    ]
    
    for file_name in possible_files:
        if os.path.exists(file_name):
            try:
                if file_name.endswith('.xlsx'):
                    # ลองอ่านแผ่นงานแรก
                    df = pd.read_excel(file_name, sheet_name=0).dropna()
                else:
                    df = pd.read_csv(file_name).dropna()
                
                # ปรับโครงสร้างข้อมูล ลบแถวว่าง แปลงเลขให้เป็น 2 หลักมี 0 นำหน้า
                df.columns = ["date", "number"]
                df["number"] = df["number"].astype(int).astype(str).str.zfill(2)
                return df, file_name
            except Exception as e:
                continue
    return None, None

df, active_file = load_lotto_data()

# ==========================================
# 3. ส่วนหัวของเว็บ RUAYDEE
# ==========================================
st.markdown(
    """
    <div class="fortune-card">
        <h1 class="fortune-title">🔮 RUAYDEE พยากรณ์เลขนำโชค 🔮</h1>
        <p style="color: #94a3b8;">เปิดมิติคำนวณตัวเลขด้วยดวงชะตาและสถิติแม่นยำ</p>
    </div>
""",
    unsafe_allow_html=True,
)

# ถ้าหาไฟล์ไม่เจอเลยจริงๆ ให้แสดงวิธีแก้ไข
if df is None:
    st.error("### ❌ ไม่พบไฟล์ข้อมูลสถิติในโฟลเดอร์")
    st.markdown(
        """
        **💡 วิธีทำให้เว็บรวยดีใช้งานได้:**
        1. ตรวจสอบว่าไฟล์หวยของคุณตั้งชื่อว่า **`to_lotto_2.xlsx`** หรือ **`to_lotto.xlsx`** หรือยัง
        2. ย้ายไฟล์นั้นมาวางไว้ในโฟลเดอร์เดียวกับโค้ดแอปนี้ที่พาธ: `D:\\Plammy\\เขียนโค้ด\\vscode\\`
        3. เมื่อวางเสร็จแล้ว ให้กดปุ่ม **Rerun** บนเบราว์เซอร์ได้เลยฮะ!
        """
    )
    st.stop()

st.markdown(
    f"""
    <div class="mascot-box">
        <b>🔮 แม่หมอพูลลี่ @ RUAYDEE:</b><br>
        "ยินดีต้อนรับสู่สำนักรวยดีฮะ! ตอนนี้ข้าเปิดคัมภีร์ดึงข้อมูลจากไฟล์ 💾 <b>{active_file}</b> สำเร็จแล้ว!<br>
        วันนี้ท่านอยากให้ข้าทำนายเลขนำโชคแบบไหนดีฮะ? เลือกปุ่มด้านล่างเพื่อรับความรวยได้เลย!"
    </div>
""",
    unsafe_allow_html=True,
)

# คำนวณเลขเด็ด 10 อันดับแรกเตรียมไว้
top_10_numbers = df["number"].value_counts().head(10).index.tolist()

# ==========================================
# 4. ฟังก์ชันการสุ่มและทำนายเลข
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎲 สายดวงดาวลิขิต")
    st.caption("สุ่มจากจักรวาลตัวเลข 00 - 99")
    btn_random = st.button("🔮 ทำนายเลขจากดวงชะตา")

with col2:
    st.markdown("### 📈 สายตำราสถิติ")
    st.caption("สุ่มดึงเฉพาะกลุ่มเลขที่ออกบ่อยที่สุด 10 อันดับแรก")
    btn_stat = st.button("📊 ทำนายเลขจากสถิติหวย")

# ส่วนแสดงผลลัพธ์คำทำนาย
st.write("---")

if btn_random:
    lucky_num = f"{random.randint(0, 99):02d}"
    st.snow()  # เอฟเฟกต์หิมะตกโทนสีเย็นสบายตา
    st.markdown(
        f"""
        <div class="fortune-card" style="border-color: #4ade80;">
            <p style="color: #4ade80; font-size: 20px;">✨ สำนักรวยดีขอมอบเลขนำโชคให้ท่านคือ ✨</p>
            <div class="lucky-number-display">{lucky_num}</div>
            <p style="color: #94a3b8; font-style: italic;">"เลขนี้เกิดจากพลังดวงดาวนำทาง ขอให้เฮง ๆ ปัง ๆ นะฮะ!"</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

elif btn_stat:
    lucky_num = random.choice(top_10_numbers)
    st.balloons()  # เอฟเฟกต์ลูกโป่งฉลองความรวย
    st.markdown(
        f"""
        <div class="fortune-card" style="border-color: #a855f7;">
            <p style="color: #a855f7; font-size: 20px;">🔥 เลขเด็ดสถิติเด่นจากคัมภีร์รวยดีคือ 🔥</p>
            <div class="lucky-number-display">{lucky_num}</div>
            <p style="color: #94a3b8; font-style: italic;">"แม่หมอคัดเลือกมาจากเลขที่ออกบ่อยที่สุดในประวัติศาสตร์ มั่นใจได้เลย!"</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="fortune-card" style="border: 1px dashed #64748b;">
            <p style="color: #64748b; font-size: 18px; margin: 40px 0;">🔮 ตั้งจิตอธิษฐาน แล้วกดปุ่มด้านบนเพื่อรับคำทำนายรวยดี 🔮</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
