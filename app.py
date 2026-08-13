import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="SmartMargin PH - E-Com Intelligence", page_icon="⚡", layout="centered")

# 2. Security System
def check_password():
    """Returns `True` if the user enters the correct client key."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Login Screen UI
    st.title("⚡ SmartMargin PH")
    st.subheader("Private Client Intelligence Portal")
    st.write("🔒 Please enter your client access key to unlock the profit engine.")
    
    password_input = st.text_input("Access Key", type="password")
    
    if st.button("Unlock Dashboard"):
        # CHANGE THIS TO YOUR CLIENT KEY!
        if password_input == "WOLF2026": 
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Invalid Access Key. Contact founder to request access.")
            
    return False

# Stop execution if password isn't correct
if not check_password():
    st.stop()

# =====================================================================
# UNLOCKED DASHBOARD AREA
# =====================================================================

st.title("⚡ SmartMargin PH")
st.subheader("Instant Profit & Marketplace Fee Calculator for PH Sellers")
st.caption("Stop guessing net profits after Shopee, Lazada, and TikTok Shop cuts!")

st.divider()

# Input Section
col1, col2 = st.columns(2)

with col1:
    item_name = st.text_input("Product Name", "Custom Mechanical Keyboard")
    selling_price = st.number_input("Selling Price (PHP)", value=1200.0, step=50.0)
    cost_price = st.number_input("Base Cost / Puhunan (PHP)", value=650.0, step=50.0)

with col2:
    platform = st.selectbox("Sales Channel", ["Shopee", "TikTok Shop", "Lazada", "Direct (FB/IG)"])
    ad_spend = st.number_input("Est. Ad Spend per Unit (PHP)", value=50.0, step=10.0)
    packaging_cost = st.number_input("Packaging & Shipping Materials (PHP)", value=25.0, step=5.0)

# Fee Rates Logic
fee_rates = {
    "Shopee": 0.12,        # ~12% combined transaction + platform fees
    "TikTok Shop": 0.10,    # ~10% platform cuts
    "Lazada": 0.11,        # ~11% commission & handling
    "Direct (FB/IG)": 0.02  # ~2% payment gateway fee
}

platform_fee = selling_price * fee_rates[platform]
total_costs = cost_price + platform_fee + ad_spend + packaging_cost
net_profit = selling_price - total_costs
profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0

st.divider()

# Output Display
st.markdown(f"### 📊 Profit Breakdown: **{item_name}**")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Gross Revenue", f"₱{selling_price:,.2f}")
col_b.metric("Platform Cut", f"₱{platform_fee:,.2f}", delta=f"-{fee_rates[platform]*100:.0f}%", delta_color="inverse")
col_c.metric("NET PROFIT", f"₱{net_profit:,.2f}", delta=f"{profit_margin:.1f}% Margin")

# Dynamic Alerts
if profit_margin < 15.0:
    st.error("🚨 DANGER: Your profit margin is below 15%! You are one ad-spend spike away from losing money on this item.")
elif profit_margin >= 30.0:
    st.success("🔥 HIGH PROFIT: This product has strong margins! You have room to run promos or undercut competitors.")
else:
    st.warning("⚠️ MODERATE: Healthy margin, but watch your platform fee adjustments closely.")

st.divider()

# Bonus Feature: Target Profit & Volume Planner
st.subheader("🎯 Goal Planner & Target Volume")
target_income = st.number_input("How much NET profit do you want to make monthly? (PHP)", value=15000.0, step=1000.0)

if net_profit > 0:
    units_needed = int(target_income / net_profit) + 1
    st.info(f"💡 To make **₱{target_income:,.2f}** clear net profit on this product, you need to sell **{units_needed} units** per month ({int(units_needed/30) + 1} sales/day).")
else:
    st.error("❌ You are currently selling at a loss! Adjust your prices or reduce cost per unit to calculate volume goals.")
