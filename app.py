import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG
# ---------------------------------------------------------
st.set_page_config(
    page_title="BOBA FACTORY",
    page_icon="🧋",
    layout="wide"
)

# Custom CSS tạo giao diện bo tròn & hiệu ứng xịn
st.markdown("""
<style>
    .main-banner {
        background: linear-gradient(135deg, #FFD1DC 0%, #FFEBEF 100%);
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #5D4037;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .sub-title {
        font-size: 16px;
        color: #8D6E63;
        font-style: italic;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DỮ LIỆU SẢN PHẨM & DỮ LIỆU MẪU
# ---------------------------------------------------------
MENU_TEA = {
    "Trà Sữa Truyền Thống": 30000,
    "Trà Sữa Trân Châu Đường Đen": 35000,
    "Trà Sữa Thái Xanh": 32000,
    "Trà Sữa Ô Long": 35000,
    "Trà Sữa Matcha": 38000,
    "Trà Sữa Dâu Tây": 35000,
    "Trà Sữa Đào": 35000,
    "Trà Sữa Dâu Tằm": 32000,
    "Trà sữa Ô Long Nướng": 40000,
    "Trà sữa Cheese Form": 40000,
}

SIZE_OPTIONS = {"MINI BATCH (Vừa)": 0, "DAILY BREW (Lớn)": 5000, "MEGA BATCH (Đặc biệt)": 10000}
TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}
SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0%"]

# Session states
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "won_gift" not in st.session_state:
    st.session_state.won_gift = ""

# ---------------------------------------------------------
# 3. THANH SIDEBAR BÊN TRÁI (GIỐNG CÁC APP VIP)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧋 BOBA ")
    st.caption("✨ Chuẩn vị trà - Thơm vị sữa - Đặt hàng nhanh chóng ✨")
    st.markdown("---")
    
    st.markdown("### 🏠 Thông tin cửa hàng")
    st.write("📍 **Địa chỉ:** 306, Võ Văn Hát, Long Trường, Thủ Đức, TP.HCM")
    st.write("⏰ **Giờ mở cửa:** 09:00 - 22:00")
    st.write("📞 **Hotline:** 0702.884.202")
    
    st.markdown("---")
    st.markdown("### 💡 Chức năng hệ thống")
    st.markdown("""
    * 🧋 Menu Gọi Món Online
    * 🎲 Vòng Quay Lucky Sip
    * 🛒 Giỏ Hàng & VietQR
    * 📊 Quản Trị Doanh Thu
    """)

# ---------------------------------------------------------
# 4. BANNER CHÍNH
# ---------------------------------------------------------
st.markdown("""
<div class="main-banner">
    <div style="font-size: 14px; letter-spacing: 3px; font-weight: bold; color: #E07A5F;">WELCOME TO OUR LITTLE WORLD</div>
    <div class="main-title">NGỌC HUỆ DRINK STUDIO</div>
    <div class="sub-title">"Tea, coffee & little joy — Một góc nhỏ ngọt ngào để bạn tìm thấy thức uống hợp mood của mình."</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. PHÂN TAB CHỨC NĂNG (MENU, LUCKY SIP, GIỎ HÀNG, QUẢN TRỊ)
# ---------------------------------------------------------
tab_menu, tab_lucky, tab_cart, tab_admin = st.tabs([
    "🧋 Menu & Gọi Món", 
    "🎁 Lucky Sip (Quay quà)", 
    f"🛒 Giỏ Hàng ({len(st.session_state.cart)})", 
    "📊 Báo Cáo Doanh Thu"
])

# ==================== TAB 1: MENU & GỌI MÓN ====================
with tab_menu:
    col_a, col_b = st.columns([1.2, 0.8])
    
    with col_a:
        st.subheader("📝 Chọn món & Khử vị")
        selected_tea = st.selectbox("Loại trà sữa:", list(MENU_TEA.keys()))
        quantity = st.number_input("Số lượng:", min_value=1, value=1)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
        with c2:
            selected_sugar = st.selectbox("Đường:", SUGAR_LEVELS)
        with c3:
            selected_ice = st.selectbox("Đá:", ICE_LEVELS)
            
        selected_toppings = st.multiselect("Topping:", list(TOPPING_OPTIONS.keys()))
        
        unit_price = MENU_TEA[selected_tea] + SIZE_OPTIONS[selected_size] + sum(TOPPING_OPTIONS[t] for t in selected_toppings)
        item_total = unit_price * quantity
        
        st.info(f"💵 Đơn giá 1 ly: **{unit_price:,} VNĐ**")
        
        if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
            st.session_state.cart.append({
                "Tên món": selected_tea,
                "Size": selected_size.split()[0],
                "Đường": selected_sugar,
                "Đá": selected_ice,
                "Topping": ", ".join(selected_toppings) if selected_toppings else "Không",
                "Đơn giá": unit_price,
                "Số lượng": quantity,
                "Thành tiền": item_total
            })
            st.session_state.invoice_paid = False
            st.toast("Đã thêm vào giỏ hàng thành công!", icon="✅")

    with col_b:
        st.subheader("🛵 Thông tin giao nhận")
        customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên bạn...")
        customer_phone = st.text_input("Số điện thoại:", placeholder="090x xxx xxx...")
        order_type = st.radio("Hình thức:", ["Tại quán", "Mang đi", "Giao hàng (Delivery)"], horizontal=True)
        delivery_address = st.text_input("Địa chỉ giao hàng (nếu có):") if order_type == "Giao hàng (Delivery)" else ""

# ==================== TAB 2: LUCKY SIP (MINIGAME) ====================
with tab_lucky:
    st.subheader("🎲 Vòng Quay May Mắn nhận Voucher")
    st.write("Quay thưởng ngay để nhận mã giảm giá cho đơn hàng hôm nay!")
    
    if st.button("🌟 Xoay Ngay Vòng Quay"):
        rewards = [("Giảm 10% tổng đơn", 10), ("Giảm 15% tổng đơn", 15), ("Giảm 20% tổng đơn", 20), ("May mắn lần sau", 0)]
        gift, disc = random.choice(rewards)
        st.session_state.game_discount = disc
        st.session_state.won_gift = gift
        
    if st.session_state.won_gift:
        st.balloons()
        st.success(f"🎉 Bạn nhận được: **{st.session_state.won_gift}**")

# ==================== TAB 3: GIỎ HÀNG & THANH TOÁN ====================
with tab_cart:
    if not st.session_state.cart:
        st.warning("Giỏ hàng hiện đang trống. Hãy qua tab Menu chọn món nhé!")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(df_cart[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]], use_container_width=True, hide_index=True)
        
        raw_total = df_cart["Thành tiền"].sum()
        ship = 15000 if order_type == "Giao hàng (Delivery)" and raw_total < 100000 else 0
        final_total = int(raw_total * (1 - st.session_state.game_discount / 100)) + ship
        
        st.markdown(f"### Tổng tiền: **{raw_total:,} VNĐ**")
        if st.session_state.game_discount > 0:
            st.markdown(f"🎁 Giảm giá Minigame ({st.session_state.game_discount}%): **-{int(raw_total * st.session_state.game_discount/100):,} VNĐ**")
        if ship > 0:
            st.markdown(f"🛵 Phí giao hàng: **{ship:,} VNĐ**")
        st.markdown(f"## THÀNH TIỀN: :red[{final_total:,} VNĐ]")
        
        payment_method = st.selectbox("Phương thức thanh toán:", ["Chuyển khoản QR ngân hàng", "Tiền mặt"])
        
        if st.button("💳 XÁC NHẬN THANH TOÁN", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            
        if st.session_state.invoice_paid:
            st.success("🎉 Đơn hàng đã được ghi nhận!")
            if payment_method == "Chuyển khoản QR ngân hàng":
                qr_url = f"https://img.vietqr.io/image/MB-0901234567-compact2.png?amount={final_total}&addInfo=TraSuaNgocHue%20{customer_phone}&accountName=NGOC%20HUE%20TEA"
                st.image(qr_url, caption="Quét mã VietQR bằng App Ngân hàng", width=300)

# ==================== TAB 4: BÁO CÁO DOANH THU ====================
with tab_admin:
    st.subheader("📊 Báo cáo Doanh thu & Thống kê")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Tổng đơn hôm nay", "12 Đơn", "+2 đơn")
    col_m2.metric("Doanh thu tạm tính", "1.450.000 VNĐ", "+15%")
    col_m3.metric("Món bán chạy nhất", "Trà Sữa Trân Châu Đường Đen")
