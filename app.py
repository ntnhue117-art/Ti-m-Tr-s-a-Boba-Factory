import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CUSTOM CSS (VIBE MINIMALIST STUDIO)
# ---------------------------------------------------------
st.set_page_config(
    page_title="BOBA FACTORY - Premium Tea Studio",
    page_icon="🧋",
    layout="wide"
)

# Custom CSS tạo giao diện bo tròn, phong cách Studio cao cấp
st.markdown("""
<style>
    .stApp {
        background-color: #FFFDF9;
    }
    
    .compact-banner {
        background: #FDF6EE;
        border: 1px solid #F5E8D9;
        padding: 22px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
    }
    .banner-title {
        font-size: 30px;
        font-weight: 800;
        color: #4A3525;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }
    .banner-sub {
        font-size: 13px;
        color: #8C7361;
        font-style: italic;
    }

    .bestseller-card {
        background-color: #FFFFFF;
        border: 1px solid #F3E5D8;
        border-radius: 18px;
        padding: 18px 15px;
        text-align: center;
    }
    
    .custom-footer {
        background-color: #FDF6EE;
        border: 1px solid #F5E8D9;
        padding: 30px;
        border-radius: 20px;
        margin-top: 40px;
        text-align: center;
        color: #4A3525;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DỮ LIỆU SẢN PHẨM & MENU PHÂN LOẠI
# ---------------------------------------------------------
MENU_DATA = {
    "Milk Tea Factory": {
        "Original Batch": {"price": 25000, "img": "🧋", "desc": "Trà sữa truyền thống - Vị trà đậm đà kết hợp béo ngậy"},
        "Brown Sugar Batch": {"price": 30000, "img": "🧋", "desc": "Trà sữa đường đen - Trân châu dẻo thơm đường đen"},
        "Golden Oolong": {"price": 29000, "img": "🫖", "desc": "Trà sữa ô long - Hương ô long thơm dịu, hậu vị thanh"}, 
        "Jasmine Silk": {"price": 27000, "img": "🧋", "desc": "Trà sữa lài - Hương hoa lài nhẹ nhàng, vị sữa béo thơm"},
        "Purple Formula": {"price": 30000, "img": "🍵", "desc": "Trà sữa khoai môn - Vị khoai môn bùi béo cùng sắc tím bắt mắt"},
        "Choco Factory": {"price": 30000, "img": "🍫", "desc": "Trà sữa chocolate - Chocolate thơm đậm hòa cùng vị trà sữa ngọt ngào"},
        "Matcha Velvet": {"price": 32000, "img": "🍵", "desc": "Trà sữa matcha - Matcha Nhật Bản nguyên chất, cân bằng bởi lớp sữa béo mịn"}
    },
    "Fresh Tea Lab": {
        "Strawberry Breeze": {"price": 29000, "img": "🍓", "desc": "Trà dâu — Hương dâu ngọt dịu, điểm chút chua nhẹ dễ uống"},
        "Peachy Mood": {"price": 27000, "img": "🍑", "desc": "Trà đào — Trà thơm dịu kết hợp vị đào ngọt thanh, tươi mát"},
        "Passion Rush": {"price": 25000, "img": "🍋", "desc": "Trà chanh dây — Chua ngọt sảng khoái, thơm nồng vị chanh dây."},
        "Citrus Spark": {"price": 27000, "img": "🍊", "desc": "Trà cam chanh — Vị cam chanh tươi sáng, chua nhẹ và thơm mát"},
        "Jasmine Peach": {"price": 27000, "img": "🍑", "desc": "Trà lài đào — Hương lài thanh tao kết hợp vị đào ngọt nhẹ"},
    }
}

BEST_SELLERS = [
    {"name": "Brown Sugar Batch", "price": 30000, "img": "🧋", "tag": "🔥 HOT Sales"},
    {"name": "Peachy Mood", "price": 27000, "img": "🍑", "tag": "⭐ Top Rated"},
    {"name": "Golden Oolong", "price": 29000, "img": "🍵", "tag": "👍 Must Try"},
    {"name": "Matcha Velvet", "price": 32000, "img": "🍵", "tag": "✨ Favorite"},
]

SIZE_OPTIONS = {"MINI BATCH (Vừa)": 0, "DAILY BREW (Lớn)": 5000, "MEGA BATCH (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Factory Pearls": {"price": 5000, "desc": "Trân châu đen"},
    "Golden Boba": {"price": 7000, "desc": "Trân châu hoàng kim"},
    "Egg Pudding": {"price": 8000, "desc": "Pudding trứng"},
    "Cloud Foam": {"price": 10000, "desc": "Kem cheese foam"},
    "Taro Bites": {"price": 8000, "desc": "Khoai môn viên"},
}
SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]

# Khởi tạo session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_item_name" not in st.session_state:
    st.session_state.selected_item_name = "Original Batch"
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "won_gift" not in st.session_state:
    st.session_state.won_gift = ""

# ---------------------------------------------------------
# 3. SIDEBAR BÊN TRÁI
# ---------------------------------------------------------
with st.sidebar:
    if os.path.exists("TRASUA.jpg"):
        st.image("TRASUA.jpg", caption="BOBA FACTORY Studio", use_container_width=True)
    
    st.markdown("## 🧋 BOBA FACTORY")
    st.caption("✨ Chuẩn vị trà - Thơm vị sữa ✨")
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
# 4. COMPACT BANNER (VIBE STUDIO BO TRÒN)
# ---------------------------------------------------------
st.markdown("""
<div class="compact-banner">
    <div style="font-size: 11px; letter-spacing: 2px; font-weight: bold; color: #C87A57;">WELCOME TO OUR TEA STUDIO</div>
    <div class="banner-title">BOBA FACTORY</div>
    <div class="banner-sub">"Trải nghiệm hương vị trà sữa thủ công đậm đà & ngọt ngào"</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. ĐIỀU HƯỚNG TAB
# ---------------------------------------------------------
tab_main, tab_lucky, tab_admin = st.tabs([
    "🧋 Đặt Hàng & Menu", 
    "🎁 Lucky Spin (Quay quà)", 
    "🔒 Trực Bếp & Quản Trị"
])

# ==================== TAB 1: TRẢI NGHIỆM ĐẶT HÀNG ====================
with tab_main:
    # --- SECTION 1: FACTORY FAVORITES ---
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
        <span style="font-size: 24px; background: #F7EBE1; padding: 8px 12px; border-radius: 12px;">⭐</span>
        <div>
            <h3 style="margin: 0; color: #4A3525; font-size: 20px;">Factory Favorites</h3>
            <p style="margin: 0; color: #8C7361; font-size: 13px;">Những công thức được yêu thích nhất</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_bs1, col_bs2, col_bs3, col_bs4 = st.columns(4)
    cols_bs = [col_bs1, col_bs2, col_bs3, col_bs4]
    
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

    # --- SECTION 2 & 3: THE BOBA LINEUP & BUILD YOUR OWN BOBA ---
    col_menu, col_custom = st.columns([1, 1.1])
    
    with col_menu:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
            <span style="font-size: 24px; background: #F7EBE1; padding: 8px 12px; border-radius: 12px;">🧋</span>
            <div>
                <h3 style="margin: 0; color: #4A3525; font-size: 20px;">The Boba Lineup</h3>
                <p style="margin: 0; color: #8C7361; font-size: 13px;">Khám phá menu đồ uống của chúng mình</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
            <span style="font-size: 24px; background: #F7EBE1; padding: 8px 12px; border-radius: 12px;">🧪</span>
            <div>
                <h3 style="margin: 0; color: #4A3525; font-size: 20px;">Build Your Own Boba</h3>
                <p style="margin: 0; color: #8C7361; font-size: 13px;">Chọn vị yêu thích, tạo ly của riêng bạn</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            })
            st.session_state.invoice_paid = False
            st.toast("Thêm vào giỏ hàng thành công!", icon="✅")

    st.markdown("---")

    # --- SECTION 4: YOUR ORDER ---
    st.markdown("### 🛒 Your Order (Giỏ Hàng & Xác Nhận Đơn)")
    
    if not st.session_state.cart:
        st.warning("Giỏ hàng hiện tại đang trống. Vui lòng chọn món ở phần menu phía trên.")
    else:
        col_cart_table, col_checkout = st.columns([1.2, 0.8])
        
        with col_cart_table:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_cart[["Tên món", "Size", "Đường", "Đá", "Topping", "Số lượng", "Thành tiền"]], use_container_width=True, hide_index=True)
            
            if st.button("🗑️ Xóa tất cả trong giỏ"):
                st.session_state.cart = []
                st.session_state.invoice_paid = False
                st.rerun()

        with col_checkout:
            st.markdown("#### 🛵 Thông tin giao nhận")
            customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên bạn...")
            customer_phone = st.text_input("Số điện thoại:", placeholder="0702xxxxxx...")
            
            # 3 Hình thức nhận hàng đúng yêu cầu
            order_type = st.radio(
                "Hình thức nhận hàng:", 
                ["Ngồi tại quán", "Đến lấy (Takeaway)", "Ship đi (Delivery)"], 
                horizontal=True
            )
            
            delivery_addr = ""
            if order_type == "Ship đi (Delivery)":
                delivery_addr = st.text_input("Địa chỉ giao hàng:", placeholder="Nhập số nhà, tên đường...")
            
            raw_total = df_cart["Thành tiền"].sum()
            ship_fee = 15000 if order_type == "Ship đi (Delivery)" and raw_total < 100000 else 0
            
            discount_amount = int(raw_total * (st.session_state.game_discount / 100))
            final_total = raw_total - discount_amount + ship_fee
            
            st.markdown(f"**Tổng tiền món:** {raw_total:,} VNĐ")
            if st.session_state.game_discount > 0:
                st.markdown(f"🎁 **Voucher giảm giá ({st.session_state.game_discount}%):** -{discount_amount:,} VNĐ")
            if ship_fee > 0:
                st.markdown(f"🛵 **Phí giao hàng:** {ship_fee:,} VNĐ")
            st.markdown(f"### TỔNG THANH TOÁN: :red[{final_total:,} VNĐ]")
            
            if st.button("💳 TẾN HÀNH THANH TOÁN", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                st.balloons()
                
            # Xử lý hiển thị mã QR theo 3 hình thức
            if st.session_state.invoice_paid:
                st.success(f"🎉 Đã ghi nhận đơn hàng cho **{customer_name if customer_name else 'Khách hàng'}** ({order_type})!")
                
                # Đến lấy hoặc Ship đi -> Hiển thị mã QR Chuyển khoản
                if order_type in ["Đến lấy (Takeaway)", "Ship đi (Delivery)"]:
                    st.markdown("#### 📲 Quét mã VietQR để thanh toán chuyển khoản")
                    qr_url = f"https://img.vietqr.io/image/MB-0702884202-compact2.png?amount={final_total}&addInfo=BOBA%20{customer_phone}&accountName=BOBA%20FACTORY"
                    st.image(qr_url, caption="Quét mã bằng App Ngân hàng / Momo để hoàn tất", width=280)
                else:
                    # Ngồi tại quán
                    st.info("💵 Bạn chọn **Ngồi tại quán**. Vui lòng thanh toán tại quầy thu ngân hoặc nhân viên phục vụ tại bàn!")

    # --- SECTION 5: FOOTER ---
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
    st.subheader("🎲 Vòng Quay May Mắn - Nhận Voucher Ngay!")
    st.write("Quay thưởng trước khi chốt đơn để săn voucher giảm giá nhé!")
    
    if st.button("🎰 THỬ VẬN MAY NGAY"):
        rewards = [("Voucher Giảm 10%", 10), ("Voucher Giảm 15%", 15), ("Voucher Giảm 20%", 20), ("Chúc bạn may mắn lần sau", 0)]
        gift, disc = random.choice(rewards)
        st.session_state.game_discount = disc
        st.session_state.won_gift = gift
        
    if st.session_state.won_gift:
        st.balloons()
        st.success(f"🎉 Kết quả quay: **{st.session_state.won_gift}** (Đã áp dụng tự động vào giỏ hàng)")

# ==================== TAB 3: QUẢN TRỊ ====================
with tab_admin:
    st.subheader("🔒 Khu Vực Quản Trị Hệ Thống & Báo Cáo")
    pin_code = st.text_input("Nhập Mã PIN Quản Trị (Mặc định: 1234):", type="password")
    
    if pin_code == "1234":
        st.success("✅ Xác thực quyền Quản trị thành công!")
        st.markdown("---")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Tổng đơn hôm nay", "18 Đơn", "+4 đơn")
        col_m2.metric("Doanh thu trong ngày", "1.890.000 VNĐ", "+22%")
        col_m3.metric("Món bán chạy nhất", "Brown Sugar Batch")
        
        st.markdown("### 📋 Danh sách đơn hàng cần pha chế (KDS)")
        if st.session_state.cart:
            st.dataframe(pd.DataFrame(st.session_state.cart), use_container_width=True)
        else:
            st.info("Hiện tại chưa có đơn hàng mới nào cần pha chế.")
    elif pin_code != "":
        st.error("❌ Mã PIN không chính xác! Vui lòng thử lại.")
