import streamlit as st
import pandas as pd
from datetime import datetime
import random
import os

# ---------------------------------------------------------
# 1. CẤU HÌNH TRANG & CƠ SỞ DỮ LIỆU SẢN PHẨM
# ---------------------------------------------------------
st.set_page_config(
    page_title="BOBA FACTORY🧋",
    page_icon="🧋",
    layout="wide"
)

# Danh sách menu & giá (VND)
MENU_TEA = {
    "Trà Sữa Truyền Thống": 30000,
    "Trà Sữa Trân Châu Đường Đen": 35000,
    "Trà Sữa Thái Xanh": 32000,
    "Trà Sữa Ô Long": 35000,
    "Trà Sữa Matcha": 38000,
    "Trà Sữa Dâu Tây": 35000,
    "Trà Đào Cam Sả": 35000,
    "Trà Dâu Tằm": 32000,
}

SIZE_OPTIONS = {
    "S (Vừa)": 0,
    "M (Lớn)": 5000,
    "L (Đặc biệt)": 10000
}

TOPPING_OPTIONS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 7000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 8000,
    "Kem Cheese": 10000
}

SUGAR_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đường)"]
ICE_LEVELS = ["100% (Bình thường)", "70%", "50%", "30%", "0% (Không đá)"]

# Khởi tạo session state
if "cart" not in st.session_state:
    st.session_state.cart = []
if "invoice_paid" not in st.session_state:
    st.session_state.invoice_paid = False
if "game_discount" not in st.session_state:
    st.session_state.game_discount = 0
if "won_gift" not in st.session_state:
    st.session_state.won_gift = ""

# ---------------------------------------------------------
# 2. HIỂN THỊ BANNER VÀ TIÊU ĐỀ
# ---------------------------------------------------------
if os.path.exists("TRASUA.jpg"):
    st.image("TRASUA.jpg", use_container_width=True)

st.title("🧋 TIỆM TRÀ SỮA NGỌC HUỆ")
st.caption("✨ Chuẩn vị trà - Thơm vị sữa - Đặt hàng nhanh chóng ✨")
st.markdown("---")

# ---------------------------------------------------------
# 3. GIAO DIỆN CHÍNH (3 CỘT)
# ---------------------------------------------------------
col_left, col_mid, col_right = st.columns([1.1, 1, 0.9])

# ==================== CỘT 1: NHẬP THÔNG TIN MÓN ====================
with col_left:
    st.subheader("📝 1. Chọn món & Tùy chọn")
    
    selected_tea = st.selectbox("Loại trà sữa:", list(MENU_TEA.keys()))
    quantity = st.number_input("Số lượng:", min_value=1, value=1, step=1)
    
    c_size, c_sugar, c_ice = st.columns(3)
    with c_size:
        selected_size = st.selectbox("Size:", list(SIZE_OPTIONS.keys()))
    with c_sugar:
        selected_sugar = st.selectbox("Mức đường:", SUGAR_LEVELS)
    with c_ice:
        selected_ice = st.selectbox("Mức đá:", ICE_LEVELS)
        
    selected_toppings = st.multiselect(
        "Topping kèm theo:",
        options=list(TOPPING_OPTIONS.keys())
    )
    
    base_price = MENU_TEA[selected_tea]
    size_price = SIZE_OPTIONS[selected_size]
    topping_price = sum(TOPPING_OPTIONS[t] for t in selected_toppings)
    unit_price = base_price + size_price + topping_price
    item_total = unit_price * quantity
    
    st.info(f"💡 Đơn giá 1 ly: **{unit_price:,} VNĐ**")
    
    if st.button("➕ Thêm vào giỏ hàng", type="primary", use_container_width=True):
        topping_str = ", ".join(selected_toppings) if selected_toppings else "Không"
        item_data = {
            "Tên món": selected_tea,
            "Size": selected_size.split()[0],
            "Đường": selected_sugar.split()[0],
            "Đá": selected_ice.split()[0],
            "Topping": topping_str,
            "Đơn giá": unit_price,
            "Số lượng": quantity,
            "Thành tiền": item_total
        }
        st.session_state.cart.append(item_data)
        st.session_state.invoice_paid = False
        st.toast(f"Đã thêm **{quantity}x {selected_tea}** vào giỏ!", icon="✅")

# ==================== CỘT 2: KHUYẾN MÃI & GIAO HÀNG ====================
with col_mid:
    st.subheader("🚚 2. Thông tin giao hàng & Ưu đãi")
    
    customer_name = st.text_input("Tên khách hàng:", placeholder="Nhập tên bạn...")
    customer_phone = st.text_input("Số điện thoại (Tích điểm):", placeholder="0901234567...")
    
    order_type = st.radio("Hình thức nhận hàng:", ["Tại quán", "Mang đi", "Giao hàng tận nơi (Delivery)"], horizontal=True)
    
    shipping_fee = 0
    delivery_address = ""
    if order_type == "Giao hàng tận nơi (Delivery)":
        delivery_address = st.text_input("Địa chỉ giao hàng:", placeholder="Nhập số nhà, tên đường...")
        shipping_fee = 15000
        st.caption("🛵 Phí ship cố định: 15.000 VNĐ (Miễn phí cho đơn từ 100k)")

    st.markdown("---")
    st.subheader("🎁 Vòng quay may mắn nhận quà")
    if st.button("🎲 Quay thưởng ngay!"):
        rewards = [
            ("Giảm 10% tổng đơn!", 10),
            ("Giảm 15% tổng đơn!", 15),
            ("Giảm 20% siêu hời!", 20),
            ("Chúc bạn may mắn lần sau!", 0)
        ]
        gift, disc_percent = random.choice(rewards)
        st.session_state.game_discount = disc_percent
        st.session_state.won_gift = gift
        
    if st.session_state.won_gift:
        st.success(f"🎉 Kết quả: **{st.session_state.won_gift}**")

# ==================== CỘT 3: GIỎ HÀNG & THANH TOÁN ====================
with col_right:
    st.subheader("🛒 3. Giỏ hàng của bạn")
    
    if not st.session_state.cart:
        st.warning("Giỏ hàng đang trống.")
    else:
        df_cart = pd.DataFrame(st.session_state.cart)
        st.dataframe(
            df_cart[["Tên món", "Size", "Số lượng", "Thành tiền"]],
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("🗑️ Xóa giỏ hàng"):
            st.session_state.cart = []
            st.session_state.invoice_paid = False
            st.rerun()
            
        raw_total = df_cart["Thành tiền"].sum()
        
        # Tính phí ship miễn phí nếu đơn >= 100k
        if raw_total >= 100000 and order_type == "Giao hàng tận nơi (Delivery)":
            shipping_fee = 0
            st.caption("🎉 Bạn được MIỄN PHÍ VẮN CHUYỂN!")
            
        manual_discount = st.number_input("Mã giảm giá thêm (%):", min_value=0, max_value=100, value=0, step=5)
        total_discount_percent = min(100, manual_discount + st.session_state.game_discount)
        
        final_price = int(raw_total * (1 - total_discount_percent / 100)) + shipping_fee
        
        st.markdown(f"**Tiền món:** {raw_total:,} VNĐ")
        if shipping_fee > 0:
            st.markdown(f"**Phí giao hàng:** {shipping_fee:,} VNĐ")
        st.markdown(f"### TỔNG CỘNG: :red[{final_price:,} VNĐ]")
        
        payment_method = st.selectbox("Phương thức thanh toán:", ["Tiền mặt khi nhận hàng", "Chuyển khoản QR ngân hàng"])
        
        if st.button("💳 XÁC NHẬN ĐẶT HÀNG", type="primary", use_container_width=True):
            st.session_state.invoice_paid = True
            st.balloons()

# ---------------------------------------------------------
# 4. HÓA ĐƠN & MÃ QR THANH TOÁN
# ---------------------------------------------------------
if st.session_state.get("invoice_paid") and st.session_state.cart:
    st.markdown("---")
    st.success("🎉 ĐẶT HÀNG THÀNH CÔNG! Dưới đây là chi tiết đơn hàng:")
    
    col_inv1, col_inv2 = st.columns([1.2, 0.8])
    
    with col_inv1:
        st.markdown("### 📄 HÓA ĐƠN BÁN HÀNG")
        st.write(f"**Thời gian:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"**Khách hàng:** {customer_name if customer_name else 'Khách vãng lai'} - **SĐT:** {customer_phone}")
        st.write(f"**Hình thức:** {order_type} {f'({delivery_address})' if delivery_address else ''}")
        
        st.table(pd.DataFrame(st.session_state.cart)[["Tên món", "Size", "Topping", "Số lượng", "Thành tiền"]])
        st.markdown(f"#### Tổng tiền thanh toán: :red[{final_price:,} VNĐ]")

    with col_inv2:
        if payment_method == "Chuyển khoản QR ngân hàng":
            st.markdown("### 📲 Quét mã VietQR thanh toán")
            # Tạo link VietQR động theo số tiền
            qr_url = f"https://img.vietqr.io/image/MB-0901234567-compact2.png?amount={final_price}&addInfo=TraSuaNgocHue%20{customer_phone}&accountName=TIEM%20TRA%20SUA%20NGOC%20HUE"
            st.image(qr_url, caption="Quét mã bằng app Ngân hàng / Momo", use_container_width=True)
        else:
            st.info("💵 Bạn đã chọn thanh toán **Tiền mặt**. Vui lòng chuẩn bị tiền khi nhận hàng!")
