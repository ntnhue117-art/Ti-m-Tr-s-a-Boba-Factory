import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os
import time

# ---------------------------------------------------------
# 1. CẤU HÌNH & KHỞI TẠO DỮ LIỆU
# ---------------------------------------------------------
st.set_page_config(page_title="BOBA FACTORY - Premium Tea Studio", page_icon="🧋", layout="wide")

# Khởi tạo session state cho các tính năng mới
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_item_name" not in st.session_state:
    st.session_state.selected_item_name = "Original Batch"
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "spins_available" not in st.session_state:
    st.session_state.spins_available = 1 # Mặc định có 1 lượt quay
if "loyalty_db" not in st.session_state:
    st.session_state.loyalty_db = {} # Lưu điểm theo SĐT
if "reviews" not in st.session_state:
    st.session_state.reviews = [
        {"name": "Minh Anh", "rating": "⭐⭐⭐⭐⭐", "cmt": "Trà sữa đậm vị, sticker dán ly cực dễ thương!"},
        {"name": "Quốc Bảo", "rating": "⭐⭐⭐⭐⭐", "cmt": "Giao hàng nhanh, trân châu mềm dẻo. Sẽ ủng hộ tiếp."}
    ]

# Dữ liệu Menu
MENU_DATA = {
    "Milk Tea Factory": {
        "Original Batch": {"price": 25000, "img": "🧋", "desc": "Trà sữa truyền thống - Vị trà đậm đà kết hợp béo ngậy"},
        "Brown Sugar Batch": {"price": 30000, "img": "🧋", "desc": "Trà sữa đường đen - Trân châu dẻo thơm đường đen"},
        "Golden Oolong": {"price": 29000, "img": "🫖", "desc": "Trà sữa ô long - Hương ô long thơm dịu, hậu vị thanh"}, 
        "Matcha Velvet": {"price": 32000, "img": "🍵", "desc": "Trà sữa matcha - Matcha Nhật Bản nguyên chất, cân bằng"}
    },
    "Fresh Tea Lab": {
        "Peachy Mood": {"price": 27000, "img": "🍑", "desc": "Trà đào — Trà thơm dịu kết hợp vị đào ngọt thanh, tươi mát"},
        "Passion Rush": {"price": 25000, "img": "🍋", "desc": "Trà chanh dây — Chua ngọt sảng khoái, thơm nồng vị chanh dây."}
    }
}

BEST_SELLERS = [
    {"name": "Brown Sugar Batch", "price": 30000, "img": "🧋", "tag": "🔥 HOT Sales"},
    {"name": "Peachy Mood", "price": 27000, "img": "🍑", "tag": "⭐ Top Rated"},
    {"name": "Golden Oolong", "price": 29000, "img": "🍵", "tag": "👍 Must Try"},
]

SIZE_OPTIONS = {"MINI BATCH (Vừa)": 0, "DAILY BREW (Lớn)": 5000, "MEGA BATCH (Đặc biệt)": 10000}
TOPPING_OPTIONS = {"Factory Pearls": 5000, "Golden Boba": 7000, "Egg Pudding": 8000, "Cloud Foam": 10000}

# CSS Custom
st.markdown("""
<style>
    .stApp { background-color: #FFFDF9; }
    .compact-banner { background: #FDF6EE; border: 1px solid #F5E8D9; padding: 22px 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .bestseller-card { background-color: #FFFFFF; border: 1px solid #F3E5D8; border-radius: 18px; padding: 18px 15px; text-align: center; }
    .review-card { background: #FFFFFF; border-left: 5px solid #E07A5F; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .happy-hour-box { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 15px; border-radius: 15px; text-align: center; color: #4A3525; font-weight: bold; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. XỬ LÝ LOGIC HAPPY HOUR (KHUNG GIỜ VÀNG)
# ---------------------------------------------------------
current_hour = datetime.now().hour
is_happy_hour = 14 <= current_hour < 16
hh_discount = 20 if is_happy_hour else 0

# ---------------------------------------------------------
# 3. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧋 BOBA FACTORY")
    
    if is_happy_hour:
        st.markdown("""
        <div class="happy-hour-box">
            ⏰ HAPPY BOBA HOUR!<br>Đang diễn ra (14:00 - 16:00)<br>Giảm tự động 20% cho mọi đơn hàng.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("⏰ **Happy Hour:** 14:00 - 16:00 hàng ngày (Giảm 20%)")
        
    st.markdown("---")
    st.write("📍 **Địa chỉ:** 306 Võ Văn Hát, P. Long Trường, TP. Thủ Đức")
    st.write("📞 **Hotline:** 0702.884.202")

# ---------------------------------------------------------
# 4. ĐIỀU HƯỚNG TAB
# ---------------------------------------------------------
st.markdown('<div class="compact-banner"><h1 style="color:#4A3525; margin:0;">BOBA FACTORY STUDIO</h1><p style="color:#8C7361; margin:0;">Trải nghiệm trà sữa thủ công & Không gian sáng tạo</p></div>', unsafe_allow_html=True)

tab_main, tab_lucky, tab_review, tab_admin = st.tabs([
    "🧋 Đặt Hàng", "🎁 Lucky Spin", "⭐ Góc Review", "🔒 KDS & Quản Trị"
])

# ==================== TAB 1: ĐẶT HÀNG ====================
with tab_main:
    # --- BEST SELLERS ---
    cols_bs = st.columns(3)
    for idx, item in enumerate(BEST_SELLERS):
        with cols_bs[idx]:
            st.markdown(f"""
            <div class="bestseller-card">
                <span style="background-color:#E07A5F; color:white; padding:3px 10px; border-radius:12px; font-size:10px;">{item['tag']}</span>
                <h2 style="margin:10px 0;">{item['img']}</h2>
                <h4>{item['name']}</h4>
                <p style="color:#C87A57; font-weight:bold;">{item['price']:,} VNĐ</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👉 Chọn món", key=f"bs_{idx}", use_container_width=True):
                st.session_state.selected_item_name = item['name']

    st.markdown("---")
    col_menu, col_custom = st.columns([1, 1.1])
    
    # --- MENU TRÁI ---
    with col_menu:
        st.subheader("🧋 The Boba Lineup")
        category = st.radio("Nhóm đồ uống:", list(MENU_DATA.keys()), horizontal=True)
        for name, info in MENU_DATA[category].items():
            c1, c2 = st.columns([3, 1])
            c1.markdown(f"**{info['img']} {name}**<br>*{info['desc']}*", unsafe_allow_html=True)
            c2.markdown(f"**:red[{info['price']:,}đ]**")
            if c2.button("Chọn", key=f"btn_{name}"):
                st.session_state.selected_item_name = name

    # --- TÙY CHỈNH PHẢI (Thêm tính năng Lời nhắn Sticker) ---
    with col_custom:
        st.subheader("🧪 Build Your Own")
        current_item = st.session_state.selected_item_name
        current_base_price = next((cat[current_item]["price"] for cat in MENU_DATA.values() if current_item in cat), 25000)
        
        st.success(f"Đang chọn: **{current_item}**")
        qty = st.number_input("Số lượng:", min_value=1, value=1)
        sz = st.selectbox("Size ly:", list(SIZE_OPTIONS.keys()))
        tops = st.multiselect("Topping:", list(TOPPING_OPTIONS.keys()))
        
        # TÍNH NĂNG 1: LỜI NHẮN TRÊN TEM LY
        sticker_note = st.text_input("📝 Lời nhắn dán ly (In lên tem KDS):", placeholder="VD: Chúc bé học tốt, Ngọt như tình yêu...")
        
        unit_price = current_base_price + SIZE_OPTIONS[sz] + sum(TOPPING_OPTIONS[t] for t in tops)
        
        if st.button("➕ THÊM VÀO GIỎ", type="primary", use_container_width=True):
            st.session_state.cart.append({
                "Tên món": current_item, "Size": sz.split()[0], "Topping": ", ".join(tops),
                "Lời nhắn": sticker_note if sticker_note else "Không",
                "SL": qty, "Đơn giá": unit_price, "Thành tiền": unit_price * qty
            })
            st.session_state.invoice_paid = False
            st.toast("Đã thêm vào giỏ!", icon="✅")

    st.markdown("---")
    
    # --- GIỎ HÀNG & THANH TOÁN (Thêm Thẻ tích điểm & Order Tracker) ---
    st.subheader("🛒 Your Order & Thanh toán")
    if st.session_state.cart:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(df_cart, use_container_width=True, hide_index=True)
        
        c_info, c_pay = st.columns([1, 1])
        with c_info:
            customer_name = st.text_input("Tên khách hàng:")
            customer_phone = st.text_input("Số điện thoại (Để tích điểm):")
            
            # TÍNH NĂNG 2: THẺ TÍCH ĐIỂM DIGITAL
            if customer_phone:
                past_cups = st.session_state.loyalty_db.get(customer_phone, 0)
                st.caption(f"🌟 **Digital Boba Card:** Bạn đã tích được **{past_cups}** ly.")
                progress = (past_cups % 10) * 10
                st.progress(progress / 100, text=f"Tiến trình: {past_cups % 10}/10 ly (Đạt 10 ly tặng 1 ly miễn phí)")

            order_type = st.radio("Nhận hàng:", ["Ngồi tại quán", "Đến lấy", "Ship đi"], horizontal=True)

        with c_pay:
            raw_total = df_cart["Thành tiền"].sum()
            total_cups_now = df_cart["SL"].sum()
            
            # Áp dụng Khuyến mãi (Lấy mức giảm cao nhất giữa Happy Hour và Lucky Spin)
            final_discount_percent = max(hh_discount, st.session_state.game_discount)
            discount_amount = int(raw_total * (final_discount_percent / 100))
            final_total = raw_total - discount_amount
            
            st.markdown(f"**Tổng tiền:** {raw_total:,} VNĐ")
            if final_discount_percent > 0:
                st.markdown(f"🎁 **Giảm giá ({final_discount_percent}%):** -{discount_amount:,} VNĐ")
            st.markdown(f"### CẦN THANH TOÁN: :red[{final_total:,} VNĐ]")
            
            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                if customer_phone:
                    st.session_state.loyalty_db[customer_phone] = st.session_state.loyalty_db.get(customer_phone, 0) + total_cups_now
                
        # TÍNH NĂNG 5: TRẠNG THÁI ĐƠN HÀNG REAL-TIME & QR CODE
        if st.session_state.invoice_paid:
            with st.status("🔄 Đang đồng bộ hệ thống...", expanded=True) as status:
                st.write("✅ Đã nhận đơn hàng")
                time.sleep(1)
                st.write("🖨️ Đang in tem dán ly & Chuyển lệnh KDS")
                time.sleep(1)
                st.write("🧑‍🍳 Barista đang chuẩn bị nguyên liệu...")
                time.sleep(1)
                status.update(label="✅ ĐƠN HÀNG ĐÃ SẴN SÀNG CHỜ XỬ LÝ TẠI QUẦY!", state="complete", expanded=False)
                
            if order_type in ["Đến lấy", "Ship đi"]:
                st.success("📲 Quét mã VietQR bên dưới để thanh toán chuyển khoản:")
                st.image(f"https://img.vietqr.io/image/MB-0702884202-compact2.png?amount={final_total}&addInfo=BOBA%20{customer_phone}", width=250)
            else:
                st.info("💵 Vui lòng thanh toán trực tiếp tại quầy hoặc tại bàn.")

# ==================== TAB 2: LUCKY SPIN ====================
with tab_lucky:
    st.subheader("🎲 Lucky Spin - Vòng quay may mắn")
    st.write(f"Bạn đang có: **{st.session_state.spins_available}** lượt quay.")
    
    if st.button("🎰 QUAY NGAY"):
        if st.session_state.spins_available > 0:
            rewards = [("Giảm 10%", 10), ("Giảm 15%", 15), ("Giảm 20%", 20), ("Trượt rồi", 0)]
            gift, disc = random.choice(rewards)
            st.session_state.game_discount = disc
            st.session_state.spins_available -= 1
            st.success(f"🎉 Kết quả: **{gift}** (Đã lưu mã vào giỏ hàng!)")
            st.balloons()
        else:
            st.warning("Bạn đã hết lượt quay! Hãy để lại Review để nhận thêm lượt nhé.")

# ==================== TAB 3: GÓC REVIEW (Thánh Trà Sữa) ====================
with tab_review:
    st.subheader("🌟 Góc Review & Bảng Xếp Hạng")
    st.write("Để lại đánh giá 5 sao để nhận ngay **1 lượt quay Lucky Spin**!")
    
    with st.form("review_form"):
        rv_name = st.text_input("Tên của bạn:")
        rv_star = st.selectbox("Đánh giá:", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"])
        rv_cmt = st.text_area("Cảm nhận của bạn về đồ uống:")
        if st.form_submit_button("Gửi Đánh Giá"):
            if rv_name and rv_cmt:
                st.session_state.reviews.insert(0, {"name": rv_name, "rating": rv_star, "cmt": rv_cmt})
                st.session_state.spins_available += 1
                st.success("Cảm ơn bạn! Đã cộng 1 lượt quay Lucky Spin vào tài khoản.")
            else:
                st.error("Vui lòng điền đủ thông tin!")
                
    st.markdown("### 🏆 Bức tường Review")
    for rv in st.session_state.reviews:
        st.markdown(f"""
        <div class="review-card">
            <strong>{rv['name']}</strong> {rv['rating']}<br>
            <i>"{rv['cmt']}"</i>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 4: KDS & QUẢN TRỊ ====================
with tab_admin:
    st.subheader("🔒 Màn hình Pha chế (KDS) & Quản trị")
    if st.text_input("Nhập Mã PIN (1234):", type="password") == "1234":
        st.success("Đăng nhập thành công!")
        st.markdown("### 🖨️ KDS - Lệnh pha chế & In tem")
        if st.session_state.cart:
            # Hiển thị trực quan cột "Lời nhắn" để Barista viết/in lên tem
            st.dataframe(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Topping", "Lời nhắn", "SL"]], use_container_width=True)
        else:
            st.info("Chưa có đơn hàng mới.")
