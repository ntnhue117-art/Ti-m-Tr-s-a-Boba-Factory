import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os
import time

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CÁC STYLE CSS (STUDIO MINIMALIST)
# ---------------------------------------------------------
st.set_page_config(
    page_title="BOBA FACTORY - Premium Tea Studio",
    page_icon="🧋",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #FFFDF9; }
    .compact-banner { background: #FDF6EE; border: 1px solid #F5E8D9; padding: 22px 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; }
    .bestseller-card { background-color: #FFFFFF; border: 1px solid #F3E5D8; border-radius: 18px; padding: 18px 15px; text-align: center; }
    .review-card { background: #FFFFFF; border-left: 5px solid #E07A5F; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .happy-hour-box { background: linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%); padding: 15px; border-radius: 15px; text-align: center; color: #4A3525; font-weight: bold; margin-bottom: 20px;}
    .custom-footer { background-color: #FDF6EE; border: 1px solid #F5E8D9; padding: 30px; border-radius: 20px; margin-top: 40px; text-align: center; color: #4A3525; }
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_item_name" not in st.session_state:
    st.session_state.selected_item_name = "Original Batch"
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "spins_available" not in st.session_state:
    st.session_state.spins_available = 1
if "loyalty_db" not in st.session_state:
    st.session_state.loyalty_db = {}
if "reviews" not in st.session_state:
    st.session_state.reviews = [
        {"name": "Minh Anh", "rating": "⭐⭐⭐⭐⭐", "cmt": "Trà sữa đậm vị, sticker dán ly cực dễ thương!"},
        {"name": "Quốc Bảo", "rating": "⭐⭐⭐⭐⭐", "cmt": "Giao hàng nhanh, trân châu mềm dẻo. Sẽ ủng hộ tiếp!"}
    ]

# Dữ liệu Menu
MENU_DATA = {
    "Milk Tea Factory": {
        "Original Batch": {"price": 25000, "img": "🧋", "desc": "Trà sữa truyền thống - Vị trà đậm đà kết hợp béo ngậy"},
        "Brown Sugar Batch": {"price": 30000, "img": "🧋", "desc": "Trà sữa đường đen - Trân châu dẻo thơm đường đen"},
        "Golden Oolong": {"price": 29000, "img": "🫖", "desc": "Trà sữa ô long - Hương ô long thơm dịu, hậu vị thanh"}, 
        "Jasmine Silk": {"price": 27000, "img": "🧋", "desc": "Trà sữa lài - Hương hoa lài nhẹ nhàng, vị sữa béo thơm"},
        "Purple Formula": {"price": 30000, "img": "🍵", "desc": "Trà sữa khoai môn - Vị khoai môn bùi béo cùng sắc tím bắt mắt"},
        "Choco Factory": {"price": 30000, "img": "🍫", "desc": "Trà sữa chocolate - Chocolate thơm đậm hòa cùng vị trà sữa"},
        "Matcha Velvet": {"price": 32000, "img": "🍵", "desc": "Trà sữa matcha - Matcha Nhật Bản nguyên chất, béo mịn"}
    },
    "Fresh Tea Lab": {
        "Strawberry Breeze": {"price": 29000, "img": "🍓", "desc": "Trà dâu — Hương dâu ngọt dịu, điểm chút chua nhẹ dễ uống"},
        "Peachy Mood": {"price": 27000, "img": "🍑", "desc": "Trà đào — Trà thơm dịu kết hợp vị đào ngọt thanh, tươi mát"},
        "Passion Rush": {"price": 25000, "img": "🍋", "desc": "Trà chanh dây — Chua ngọt sảng khoái, thơm nồng chanh dây"},
        "Citrus Spark": {"price": 27000, "img": "🍊", "desc": "Trà cam chanh — Vị cam chanh tươi sáng, chua nhẹ thơm mát"},
        "Jasmine Peach": {"price": 27000, "img": "🍑", "desc": "Trà lài đào — Hương lài thanh tao kết hợp vị đào ngọt nhẹ"}
    }
}

BEST_SELLERS = [
    {"name": "Brown Sugar Batch", "price": 30000, "img": "🧋", "tag": "🔥 HOT Sales"},
    {"name": "Peachy Mood", "price": 27000, "img": "🍑", "tag": "⭐ Top Rated"},
    {"name": "Golden Oolong", "price": 29000, "img": "🍵", "tag": "👍 Must Try"},
    {"name": "Matcha Velvet", "price": 32000, "img": "🍵", "tag": "✨ Favorite"}
]

SIZE_OPTIONS = {"MINI BATCH (Vừa)": 0, "DAILY BREW (Lớn)": 5000, "MEGA BATCH (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Factory Pearls": {"price": 5000, "desc": "Trân châu đen"},
    "Golden Boba": {"price": 7000, "desc": "Trân châu hoàng kim"},
    "Egg Pudding": {"price": 8000, "desc": "Pudding trứng"},
    "Cloud Foam": {"price": 10000, "desc": "Kem cheese foam"},
    "Taro Bites": {"price": 8000, "desc": "Khoai môn viên"}
}
SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]

# Khung giờ vàng Happy Hour
current_hour = datetime.now().hour
is_happy_hour = 14 <= current_hour < 16
hh_discount = 20 if is_happy_hour else 0

# ---------------------------------------------------------
# 2. SIDEBAR BÊN TRÁI (LOGO & THÔNG TIN QUÁN)
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("TRASUA.jpg"):
        st.image("TRASUA.jpg", caption="BOBA FACTORY Studio", use_container_width=True)
    
    st.markdown("## 🧋 BOBA FACTORY")
    st.caption("✨ Chuẩn vị trà - Thơm vị sữa ✨")
    
    if is_happy_hour:
        st.markdown("""
        <div class="happy-hour-box">
            ⏰ HAPPY BOBA HOUR!<br>Đang diễn ra (14:00 - 16:00)<br>Giảm tự động 20% cho mọi đơn hàng!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("⏰ **Happy Hour:** 14:00 - 16:00 hàng ngày (Giảm 20%)")
        
    st.markdown("---")
    st.markdown("### 🏠 Thông tin cửa hàng")
    st.write("📍 **Địa chỉ:** 306 Võ Văn Hát, P. Long Trường, TP. Thủ Đức, TP.HCM")
    st.write("⏰ **Giờ mở cửa:** 09:00 - 22:00")
    st.write("📞 **Hotline/Zalo:** 0702.884.202")
    
    st.markdown("---")
    st.markdown("### 💳 Thông tin chuyển khoản")
    st.write("🏦 **Ngân hàng:** MB Bank / Momo")
    st.write("👤 **Chủ tài khoản:** BOBA FACTORY")
    st.write("🔢 **Số tài khoản:** **0702884202**")

# ---------------------------------------------------------
# 3. COMPACT BANNER
# ---------------------------------------------------------
st.markdown("""
<div class="compact-banner">
    <div style="font-size: 11px; letter-spacing: 2px; font-weight: bold; color: #C87A57;">WELCOME TO OUR TEA STUDIO</div>
    <div style="font-size: 30px; font-weight: 800; color: #4A3525; letter-spacing: 2px;">BOBA FACTORY</div>
    <div style="font-size: 13px; color: #8C7361; font-style: italic;">"Trải nghiệm hương vị trà sữa thủ công đậm đà & ngọt ngào"</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. ĐIỀU HƯỚNG TAB
# ---------------------------------------------------------
tab_main, tab_lucky, tab_review, tab_admin = st.tabs([
    "🧋 Đặt Hàng & Menu", 
    "🎁 Lucky Spin (Quay quà)", 
    "⭐ Góc Review & Bảng Xếp Hạng",
    "🔒 Trực Bếp & Quản Trị"
])

# ==================== TAB 1: TRẢI NGHIỆM ĐẶT HÀNG ====================
with tab_main:
    # --- FACTORY FAVORITES ---
    st.markdown("### ⭐ Factory Favorites (Những công thức được yêu thích nhất)")
    cols_bs = st.columns(4)
    for idx, item in enumerate(BEST_SELLERS):
        with cols_bs[idx]:
            st.markdown(f"""
            <div class="bestseller-card">
                <span style="background-color:#E07A5F; color:white; padding:3px 10px; border-radius:12px; font-size:10px; font-weight:bold;">{item['tag']}</span>
                <h2 style="margin:10px 0; font-size:40px;">{item['img']}</h2>
                <h4 style="font-size:14px; margin:5px 0; color:#4A3525;">{item['name']}</h4>
                <p style="color:#C87A57; font-weight:bold; margin-bottom:10px;">{item['price']:,} VNĐ</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("👉 Chọn món này", key=f"bs_{idx}", use_container_width=True):
                st.session_state.selected_item_name = item['name']
                st.toast(f"Đã chọn **{item['name']}**!", icon="🎯")

    st.markdown("---")

    # --- THE BOBA LINEUP & BUILD YOUR OWN BOBA ---
    col_menu, col_custom = st.columns([1, 1.1])
    
    with col_menu:
        st.markdown("### 🧋 The Boba Lineup (Khám phá menu đồ uống)")
        category = st.radio("Chọn nhóm đồ uống:", list(MENU_DATA.keys()), horizontal=True)
        
        selected_category_items = MENU_DATA[category]
        for name, info in selected_category_items.items():
            c_m1, c_m2, c_m3 = st.columns([1, 3, 1.5])
            c_m1.markdown(f"# {info['img']}")
            c_m2.markdown(f"**{name}**\n\n*{info['desc']}*")
            c_m3.markdown(f"**:red[{info['price']:,} VNĐ]**")
            if c_m3.button("Chọn", key=f"btn_{name}"):
                st.session_state.selected_item_name = name
                st.toast(f"Đã chọn: {name}", icon="🧋")
            st.divider()

    with col_custom:
        st.markdown("### 🧪 Build Your Own Boba (Chọn vị yêu thích, tạo ly riêng)")
        
        current_item = st.session_state.selected_item_name
        current_base_price = 25000
        for cat in MENU_DATA.values():
            if current_item in cat:
                current_base_price = cat[current_item]["price"]
                break
                
        st.success(f"Món đang chọn: **{current_item}** ({current_base_price:,} VNĐ)")
        
        quantity = st.number_input("Số lượng:", min_value=1, value=1)
        
        c_sz, c_sg, c_ic = st.columns(3)
        with c_sz:
            selected_size = st.selectbox("Size ly:", list(SIZE_OPTIONS.keys()))
        with c_sg:
            selected_sugar = st.selectbox("Mức đường:", SUGAR_LEVELS)
        with c_ic:
            selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)
            
        selected_toppings = st.multiselect(
            "Thêm Topping:", 
            options=list(TOPPING_OPTIONS.keys()),
            format_func=lambda x: f"{x} ({TOPPING_OPTIONS[x]['desc']} - +{TOPPING_OPTIONS[x]['price']:,}đ)"
        )
        
        sticker_note = st.text_input("📝 Lời nhắn dán lên tem ly (Custom Sticker):", placeholder="VD: Chúc bé học tốt, Ngọt 50% như tình yêu...")
        
        topping_price = sum(TOPPING_OPTIONS[t]["price"] for t in selected_toppings)
        unit_price = current_base_price + SIZE_OPTIONS[selected_size] + topping_price
        item_total = unit_price * quantity
        
        st.info(f"💰 Đơn giá 1 ly tùy chỉnh: **{unit_price:,} VNĐ**")
        
        if st.button("➕ THÊM VÀO GIỎ HÀNG", type="primary", use_container_width=True):
            st.session_state.cart.append({
                "Tên món": current_item,
                "Size": selected_size.split()[0],
                "Đường": selected_sugar.split()[0],
                "Đá": selected_ice.split()[0],
                "Topping": ", ".join(selected_toppings) if selected_toppings else "Không",
                "Lời nhắn Sticker": sticker_note if sticker_note else "Không",
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            })
            st.session_state.invoice_paid = False
            st.toast("Thêm vào giỏ hàng thành công!", icon="✅")

    st.markdown("---")

    # --- YOUR ORDER (GIỎ HÀNG & XÁC NHẬN) ---
    st.markdown("### 🛒 Your Order (Giỏ Hàng & Xác Nhận Đơn)")
    
    if not st.session_state.cart:
        st.warning("Giỏ hàng hiện tại đang trống. Vui lòng chọn món ở phần menu phía trên.")
    else:
        col_cart_table, col_checkout = st.columns([1.2, 0.8])
        
        with col_cart_table:
            df_cart = pd.DataFrame(st.session_state.cart)
            
            # Xử lý hiển thị bảng an toàn phòng trường hợp giỏ hàng còn dữ liệu cũ
            cols_to_show = [c for c in ["Tên món", "Size", "Topping", "Lời nhắn Sticker", "Số lượng", "Thành tiền"] if c in df_cart.columns]
            st.dataframe(df_cart[cols_to_show], use_container_width=True, hide_index=True)
            
            if st.button("🗑️ Xóa tất cả trong giỏ"):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()

        with col_checkout:
            st.markdown("#### 🛵 Thông tin giao nhận")
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên bạn...")
            customer_phone = st.text_input("Số điện thoại (Tích điểm):", placeholder="0702xxxxxx...")
            
            if customer_phone:
                past_cups = st.session_state.loyalty_db.get(customer_phone, 0)
                st.caption(f"🌟 **Digital Stamp Card:** Đã tích **{past_cups}** ly.")
                st.progress((past_cups % 10) / 10, text=f"Tiến trình: {past_cups % 10}/10 ly (Đạt 10 ly tặng 1 ly miễn phí)")

            order_type = st.radio("Hình thức nhận hàng:", ["Ngồi tại quán", "Đến lấy (Takeaway)", "Ship đi (Delivery)"], horizontal=True)
            
            delivery_addr = ""
            if order_type == "Ship đi (Delivery)":
                delivery_addr = st.text_input("Địa chỉ giao hàng:", placeholder="Nhập số nhà, tên đường...")
            
            raw_total = df_cart["Thành tiền"].sum()
            total_cups_now = df_cart["Số lượng"].sum()
            ship_fee = 15000 if order_type == "Ship đi (Delivery)" and raw_total < 100000 else 0
            
            final_discount_percent = max(hh_discount, st.session_state.game_discount)
            discount_amount = int(raw_total * (final_discount_percent / 100))
            final_total = raw_total - discount_amount + ship_fee
            
            st.markdown(f"**Tổng tiền món:** {raw_total:,} VNĐ")
            if final_discount_percent > 0:
                st.markdown(f"🎁 **Giảm giá ({final_discount_percent}%):** -{discount_amount:,} VNĐ")
            if ship_fee > 0:
                st.markdown(f"🛵 **Phí giao hàng:** {ship_fee:,} VNĐ")
            st.markdown(f"### TỔNG THANH TOÁN: :red[{final_total:,} VNĐ]")
            
            if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                if customer_phone:
                    st.session_state.loyalty_db[customer_phone] = st.session_state.loyalty_db.get(customer_phone, 0) + total_cups_now
                st.balloons()
                
        # Order Tracker & VietQR
        if st.session_state.invoice_paid:
            with st.status("🔄 Đang xử lý đơn hàng theo thời gian thực...", expanded=True) as status:
                st.write("✅ Đã nhận thông tin đơn hàng")
                time.sleep(0.8)
                st.write("🖨️ Đang in tem dán ly (Sticker) & Chuyển lệnh xuống bếp")
                time.sleep(0.8)
                st.write("🧑‍🍳 Barista đang tiến hành pha chế...")
                time.sleep(0.8)
                status.update(label="🎉 ĐƠN HÀNG ĐÃ HOÀN TẤT & SẴN SÀNG!", state="complete", expanded=False)

            if order_type in ["Đến lấy (Takeaway)", "Ship đi (Delivery)"]:
                st.markdown("#### 📲 Quét mã VietQR Chuyển Khoản")
                qr_url = f"https://img.vietqr.io/image/MB-0702884202-compact2.png?amount={final_total}&addInfo=BOBA%20{customer_phone}&accountName=BOBA%20FACTORY"
                st.image(qr_url, caption="Mở App Ngân hàng / Momo quét mã để hoàn tất", width=280)
            else:
                st.info("💵 Bạn chọn **Ngồi tại quán**. Vui lòng thanh toán trực tiếp tại quầy thu ngân hoặc tại bàn!")

    # --- FOOTER ---
    st.markdown("""
    <div class="custom-footer">
        <h3>🧋 BOBA FACTORY STUDIO</h3>
        <p>📍 <b>Địa chỉ:</b> 306 Võ Văn Hát, P. Long Trường, TP. Thủ Đức, TP.HCM</p>
        <p>📞 <b>Hotline Đặt Hàng:</b> 0702.884.202 | ⏰ <b>Mở cửa:</b> 09:00 - 22:00 Hàng ngày</p>
        <p style="font-size: 13px; color: #8D6E63; margin-top: 10px;">© 2026 BOBA FACTORY. Designed with ❤️ by Ngoc Hue</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 2: LUCKY SPIN ====================
with tab_lucky:
    st.subheader("🎲 Vòng Quay May Mắn - Săn Voucher Ngay")
    st.write(f"Số lượt quay hiện tại của bạn: **{st.session_state.spins_available}** lượt.")
    
    if st.button("🎰 TỰ QUAY NGAY"):
        if st.session_state.spins_available > 0:
            rewards = [("Voucher Giảm 10%", 10), ("Voucher Giảm 15%", 15), ("Voucher Giảm 20%", 20), ("May mắn lần sau", 0)]
            gift, disc = random.choice(rewards)
            st.session_state.game_discount = disc
            st.session_state.spins_available -= 1
            st.success(f"🎉 Kết quả: **{gift}** (Đã lưu mã giảm vào giỏ hàng!)")
            st.balloons()
        else:
            st.warning("Bạn đã hết lượt quay! Hãy viết đánh giá tại tab 'Góc Review' để nhận thêm lượt nhé.")

# ==================== TAB 3: GÓC REVIEW & BẢNG XẾP HẠNG ====================
with tab_review:
    st.subheader("🌟 Góc Review & Bảng Xếp Hạng Thánh Trà Sữa")
    st.write("Gửi nhận xét 5 sao để nhận ngay **1 lượt quay Lucky Spin**!")
    
    with st.form("review_form"):
        rv_name = st.text_input("Tên của bạn:")
        rv_star = st.selectbox("Đánh giá:", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"])
        rv_cmt = st.text_area("Cảm nhận của bạn về trà sữa BOBA FACTORY:")
        if st.form_submit_button("Gửi Đánh Giá"):
            if rv_name and rv_cmt:
                st.session_state.reviews.insert(0, {"name": rv_name, "rating": rv_star, "cmt": rv_cmt})
                st.session_state.spins_available += 1
                st.success("Cảm ơn bạn! Đã thưởng 1 lượt quay Lucky Spin vào tài khoản.")
            else:
                st.error("Vui lòng nhập đầy đủ thông tin trước khi gửi!")

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
    st.subheader("🔒 Khu Vực Quản Trị & Màn Hình Pha Chế (KDS)")
    pin_code = st.text_input("Nhập Mã PIN Quản Trị (Mặc định: 1234):", type="password")
    
    if pin_code == "1234":
        st.success("✅ Xác thực quyền Quản trị thành công!")
        st.markdown("---")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Tổng đơn hôm nay", "18 Đơn", "+4 đơn")
        col_m2.metric("Doanh thu trong ngày", "1.890.000 VNĐ", "+22%")
        col_m3.metric("Món bán chạy nhất", "Brown Sugar Batch")
        
        st.markdown("### 🖨️ KDS - Danh sách đơn hàng & In tem sticker ly")
        if st.session_state.cart:
            df_kds = pd.DataFrame(st.session_state.cart)
            cols_kds = [c for c in ["Tên món", "Size", "Topping", "Lời nhắn Sticker", "Số lượng"] if c in df_kds.columns]
            st.dataframe(df_kds[cols_kds], use_container_width=True)
        else:
            st.info("Hiện tại chưa có đơn hàng mới nào cần pha chế.")
    elif pin_code != "":
        st.error("❌ Mã PIN không chính xác! Vui lòng thử lại.")
