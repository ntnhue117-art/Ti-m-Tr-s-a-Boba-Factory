import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="BOBA FACTORY - Premium Tea Studio",
    page_icon="🧋",
    layout="wide"
)

# Custom CSS thu gọn Banner & làm đẹp UI
st.markdown("""
<style>
    /* Thu gọn Banner 25% chiều cao */
    .compact-banner {
        background: linear-gradient(135deg, #FFD1DC 0%, #FFEBEF 100%);
        padding: 18px 25px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }
    .banner-title {
        font-size: 32px;
        font-weight: 800;
        color: #5D4037;
        margin-bottom: 2px;
        letter-spacing: 2px;
    }
    .banner-sub {
        font-size: 14px;
        color: #8D6E63;
        font-style: italic;
    }
    /* Thẻ Best Seller */
    .bestseller-card {
        background-color: #FFFFFF;
        border: 1px solid #F4E4D4;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    /* Footer */
    .custom-footer {
        background-color: #F5E6D3;
        padding: 25px;
        border-radius: 15px;
        margin-top: 40px;
        text-align: center;
        color: #5D4037;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DỮ LIỆU SẢN PHẨM & MENU PHÂN LOẠI
# ---------------------------------------------------------
MENU_DATA = {
    "Trà Sữa": {
        "Trà Sữa Truyền Thống": {"price": 30000, "img": "🧋", "desc": "Vị trà đậm đà kết hợp béo ngậy"},
        "Trà Sữa Trân Châu Đường Đen": {"price": 35000, "img": "🧋", "desc": "Trân châu dẻo thơm đường đen"},
        "Trà Sữa Thái Xanh": {"price": 32000, "img": "🍵", "desc": "Thơm mát chuẩn vị Thái"},
        "Trà Sữa Ô Long": {"price": 35000, "img": "🧋", "desc": "Hương ô long thanh nhẹ, đậm hậu vị"},
        "Trà Sữa Matcha": {"price": 38000, "img": "🍵", "desc": "Matcha Nhật Bản nguyên chất"}
    },
    "Trà Trái Cây": {
        "Trà Đào Cam Sả": {"price": 35000, "img": "🍑", "desc": "Giải nhiệt ngày hè với miếng đào giòn"},
        "Trà Dâu Tằm": {"price": 32000, "img": "🍓", "desc": "Chua ngọt tự nhiên từ dâu tằm tươi"},
        "Trà Dâu Tây": {"price": 35000, "img": "🍓", "desc": "Hương dâu tây tươi mát bộc phá"}
    }
}

BEST_SELLERS = [
    {"name": "Trà Sữa Trân Châu Đường Đen", "price": 35000, "img": "🧋", "tag": "🔥 HOT Sales"},
    {"name": "Trà Đào Cam Sả", "price": 35000, "img": "🍑", "tag": "⭐ Top Rated"},
    {"name": "Trà Sữa Ô Long", "price": 35000, "img": "🍵", "tag": "👍 Must Try"},
    {"name": "Trà Sữa Matcha", "price": 38000, "img": "🍵", "tag": "✨ Favorite"}
]

SIZE_OPTIONS = {"S (Vừa)": 0, "M (Lớn)": 5000, "L (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}
SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]

# Khởi tạo session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_item_name" not in st.session_state:
    st.session_state.selected_item_name = "Trà Sữa Truyền Thống"
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "won_gift" not in st.session_state:
    st.session_state.won_gift = ""

# ---------------------------------------------------------
# 3. SIDEBAR BÊN TRÁI (LOGO NHỎ & THÔNG TIN CỬA HÀNG)
# ---------------------------------------------------------
with st.sidebar:
    # Đưa ảnh cửa hàng vào 1 góc nhỏ ở sidebar
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
# 4. COMPACT BANNER (ĐÃ THU GỌN 25% CHIỀU CAO)
# ---------------------------------------------------------
st.markdown("""
<div class="compact-banner">
    <div style="font-size: 12px; letter-spacing: 2px; font-weight: bold; color: #E07A5F;">WELCOME TO OUR TEA STUDIO</div>
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
    # --- BỐ CỤC 1: BEST SELLERS ---
    st.markdown("### 1. 🔥 Best Sellers (Món Bán Chạy)")
    col_bs1, col_bs2, col_bs3, col_bs4 = st.columns(4)
    cols_bs = [col_bs1, col_bs2, col_bs3, col_bs4]
    
    for idx, item in enumerate(BEST_SELLERS):
        with cols_bs[idx]:
            st.markdown(f"""
            <div class="bestseller-card">
                <span style="background-color:#E07A5F; color:white; padding:2px 8px; border-radius:10px; font-size:11px;">{item['tag']}</span>
                <h3 style="margin:8px 0; font-size:45px;">{item['img']}</h3>
                <h4 style="font-size:15px; margin:5px 0;">{item['name']}</h4>
                <p style="color:#E07A5F; font-weight:bold; margin-bottom:8px;">{item['price']:,} VNĐ</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"👉 Chọn món này", key=f"bs_{idx}", use_container_width=True):
                st.session_state.selected_item_name = item['name']
                st.toast(f"Đã chọn **{item['name']}**! Hãy chọn tùy chọn bên dưới.", icon="🎯")

    st.markdown("---")

    # --- BỐ CỤC 2: EXPLORE THE MENU & 3: CUSTOMIZE YOUR CUP ---
    col_menu, col_custom = st.columns([1, 1.1])
    
    with col_menu:
        st.markdown("### 2. 🧋 Explore the Menu (Khám Phá Menu)")
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
        st.markdown("### 3. 🎨 Customize Your Cup (Tùy Chỉnh Ly Trà Sữa)")
        
        # Tìm giá của món đang chọn
        current_item = st.session_state.selected_item_name
        current_base_price = 30000
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
            
        selected_toppings = st.multiselect("Thêm Topping:", list(TOPPING_OPTIONS.keys()))
        
        unit_price = current_base_price + SIZE_OPTIONS[selected_size] + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
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

    # --- BỐ CỤC 4: YOUR ORDER (GIỎ HÀNG & THANH TOÁN) ---
    st.markdown("### 4. 🛒 Your Order (Giỏ Hàng & Xác Nhận Đơn)")
    
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
            order_type = st.radio("Hình thức:", ["Tại quán", "Mang đi", "Giao hàng (Delivery)"], horizontal=True)
            delivery_addr = st.text_input("Địa chỉ giao hàng:") if order_type == "Giao hàng (Delivery)" else ""
            
            raw_total = df_cart["Thành tiền"].sum()
            ship_fee = 15000 if order_type == "Giao hàng (Delivery)" and raw_total < 100000 else 0
            
            discount_amount = int(raw_total * (st.session_state.game_discount / 100))
            final_total = raw_total - discount_amount + ship_fee
            
            st.markdown(f"**Tổng tiền món:** {raw_total:,} VNĐ")
            if st.session_state.game_discount > 0:
                st.markdown(f"🎁 **Voucher giảm giá ({st.session_state.game_discount}%):** -{discount_amount:,} VNĐ")
            if ship_fee > 0:
                st.markdown(f"🛵 **Phí giao hàng:** {ship_fee:,} VNĐ")
            st.markdown(f"### TỔNG THANH TOÁN: :red[{final_total:,} VNĐ]")
            
            payment_method = st.selectbox("Phương thức thanh toán:", ["Chuyển khoản VietQR", "Tiền mặt"])
            
            if st.button("💳 XÁC NHẬN ĐẶT HÀNG", type="primary", use_container_width=True):
                st.session_state.invoice_paid = True
                st.balloons()
                
            if st.session_state.invoice_paid:
                st.success("🎉 Đơn hàng của bạn đã được gửi thành công!")
                if payment_method == "Chuyển khoản VietQR":
                    st.markdown("#### 📲 Quét mã VietQR Chuyển Khoản")
                    # Tạo mã VietQR động
                    qr_url = f"https://img.vietqr.io/image/MB-0702884202-compact2.png?amount={final_total}&addInfo=BOBA%20{customer_phone}&accountName=BOBA%20FACTORY"
                    st.image(qr_url, caption="Mở App Ngân hàng quét mã chuyển khoản", width=280)

    # --- BỐ CỤC 5: FOOTER ---
    st.markdown("""
    <div class="custom-footer">
        <h3>🧋 BOBA FACTORY STUDIO</h3>
        <p>📍 <b>Địa chỉ:</b> 306 Võ Văn Hát, P. Long Trường, TP. Thủ Đức, TP.HCM</p>
        <p>📞 <b>Hotline Đặt Hàng:</b> 0702.884.202 | ⏰ <b>Mở cửa:</b> 09:00 - 22:00 Hàng ngày</p>
        <p style="font-size: 13px; color: #8
