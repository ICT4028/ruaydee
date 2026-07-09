import os
import random
from datetime import datetime
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บเปิดตัวให้สวยงาม
st.set_page_config(page_title="RUAYDEE - สำนักพยากรณ์เลขนำโชค", page_icon="🔮", layout="centered")

FILE_NAME = "to_lotto.csv"

def load_data():
    if not os.path.exists(FILE_NAME):
        st.error(f"❌ ไม่พบไฟล์ข้อมูล {FILE_NAME} ในระบบ")
        return None
    # สุ่มตรวจหาการเข้ารหัสภาษาที่รองรับ Excel บน Windows
    encodings = ['utf-8', 'utf-8-sig', 'cp874', 'windows-1256']
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(FILE_NAME, encoding=enc)
            break
        except:
            continue
    if df is None:
        return None
    
    df = df.dropna(subset=[df.columns[0], df.columns[1]])
    history = []
    for _, row in df.iterrows():
        date_str = str(row.iloc[0]).strip().split(" ")[0]
        try:
            num_str = str(int(float(row.iloc[1]))).zfill(2)
            history.append({"date": date_str, "number": num_str})
        except:
            continue
    return history

# --- เริ่มต้นหน้าเว็บสำนักพยากรณ์ ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🔮 RUAYDEE พยากรณ์เลขนำโชค 🔮</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>มิติใหม่แห่งการคำนวณหวยด้วยระบบ Streamlit Web Application ✨</p>", unsafe_allow_html=True)

history_data = load_data()

if history_data:
    all_numbers = [item["number"] for item in history_data]
    top_10 = pd.Series(all_numbers).value_counts().head(10).index.tolist() if all_numbers else []
    
    st.info("🔮 **แม่หมอพูลลี่:** ยินดีต้อนรับสู่สำนักเวอร์ชันออนไลน์ฮะ! คัมภีร์ข้อมูลพร้อมแล้ว กดทำนายหรือเลือกวันล่วงหน้าได้เลยจ้า!")

    # --- ฟีเจอร์: เลือกวันทำนายหวยอนาคต ---
    st.markdown("### 📅 คัมภีร์หยั่งรู้อนาคต (เจาะจงวัน)")
    chosen_date = st.date_input("เลือกวันที่หวยจะออกในอนาคตเพื่อคำนวณสถิติย้อนรอยวันนั้นๆ:")
    
    if st.button("🌸 เจาะเวลาหาเลขเด็ดอนาคต", use_container_width=True):
        target_day = str(chosen_date.day).zfill(2)
        matched = [item["number"] for item in history_data if item["date"].split("-")[-1] == target_day]
        
        if matched:
            lucky_num = pd.Series(matched).value_counts().index[0]
        else:
            lucky_num = random.choice(top_10) if top_10 else str(random.randint(0, 99)).zfill(2)
            
        st.markdown(f"""
        <div style="background: rgba(236, 72, 153, 0.1); border: 2px solid #ec4899; padding: 20px; border-radius: 15px; text-align: center; margin: 15px 0;">
            <p style="color: #ec4899; font-size: 20px; margin: 0;">🔮 ผลลัพธ์เจาะเวลาสู่งวดวันที่ {chosen_date.strftime('%d/%m/%Y')} 🔮</p>
            <h1 style="font-size: 60px; color: #ec4899; margin: 10px 0; text-shadow: 0 0 15px rgba(236,72,153,0.5);">{lucky_num}</h1>
            <p style="color: #e2e8f0; font-size: 14px; margin: 0;">"แม่หมอย้อนไปสืบสถิติรางวัลในอดีตที่เคยตรงกับวันดังกล่าวมาให้ท่านแล้ว ขอให้โชคดีฮะ!"</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px dashed #334155;'>", unsafe_allow_html=True)

    # --- ฟังก์ชันทำนายเลขสุ่ม & สถิติเดิม ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🎲 สายดวงดาวลิขิต")
        if st.button("🔮 ทำนายเลขจากดวงชะตา", use_container_width=True):
            lucky_num = str(random.randint(0, 99)).zfill(2)
            st.markdown(f"""
            <div style="border: 2px solid #4ade80; padding: 15px; border-radius: 15px; text-align: center; margin-top: 10px;">
                <h2 style="color: #4ade80; margin: 0;">{lucky_num}</h2>
                <small style="color: #94a3b8;">เลขดวงดาวนำทาง ขอให้เฮงๆ ปังๆ ฮะ!</small>
            </div>
            """, unsafe_allow_html=True)
            
    with col2:
        st.markdown("##### 📈 สายตำราสถิติ")
        if st.button("📊 ทำนายเลขจากสถิติหวย", use_container_width=True):
            lucky_num = random.choice(top_10) if top_10 else str(random.randint(0, 99)).zfill(2)
            st.markdown(f"""
            <div style="border: 2px solid #a855f7; padding: 15px; border-radius: 15px; text-align: center; margin-top: 10px;">
                <h2 style="color: #a855f7; margin: 0;">{lucky_num}</h2>
                <small style="color: #94a3b8;">คัดจากเลขที่ออกบ่อยที่สุดในประวัติศาสตร์!</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px solid #334155;'>", unsafe_allow_html=True)

    # --- คัมภีร์ตรวจหวยย้อนหลัง ---
    st.markdown("### 📜 คัมภีร์ตรวจหวยย้อนหลัง")
    limit = st.selectbox("เลือกจำนวนงวดที่ต้องการดู:", [5, 10, 20, 50])
    
    df_display = pd.DataFrame(history_data[:limit])
    df_display.columns = ["📅 งวดประจำวันที่", "💰 เลขท้าย 2 ตัวที่ออก"]
    st.dataframe(df_display, use_container_width=True, hide_index=True)