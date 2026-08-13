import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="SmartMargin PH - E-Com Intelligence", page_icon="⚡", layout="centered")

# 2. Gatekeeper Security System
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("⚡ SmartMargin PH")
    st.subheader("Private Client Intelligence Portal")
    st.write("🔒 Please enter your client access key to unlock the profit engine.")
    
    password_input = st.text_input("Access Key", type="password")
    
    if st.button("Unlock Dashboard"):
        if password_input == "WOLF2026": 
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Invalid Access Key. Contact founder to request access.")
            
    return False

if not check_password():
    st.stop()

# =====================================================================
# UNLOCKED DASHBOARD AREA
# =====================================================================

st.title("⚡ SmartMargin PH")
st.subheader("Instant Profit & Marketplace Fee Calculator for PH Sellers")
st.caption("Accurate Net Margin Calculations Accounting for Local Marketplace Cuts")

st.divider()

# Input Section with GRAYED-OUT PLACEHOLDERS (No real hardcoded defaults)
col1, col2 = st.columns(2)

with col1:
    item_name = st.text_input("Product Name", placeholder="e.g. Wireless Earbuds")
    selling_price = st.number_input("Selling Price (PHP)", value=None, placeholder="e.g. 1200.00")
    cost_price = st.number_input("Base Cost / Puhunan (PHP)", value=None, placeholder="e.g. 650.00")

with col2:
    platform = st.selectbox("Sales Channel", ["Shopee", "TikTok Shop", "Lazada", "Direct (FB/IG)"])
    ad_spend = st.number_input("Est. Ad Spend per Unit (PHP)", value=0.0, placeholder="e.g. 50.00")
    packaging_cost = st.number_input("Packaging & Shipping Materials (PHP)", value=0.0, placeholder="e.g. 25.00")

# Fee Rates Logic (Based on official PH Seller Center Fee Schedules)
fee_rates = {
    "Shopee": 0.12,        # Combined Commission (5-7%) + Transaction Fee (2.24%) + Service Programs
    "TikTok Shop": 0.10,    # Marketplace Commission + Transaction Service Cuts
    "Lazada": 0.11,        # Marketplace Commission + Gateway Handling + Free Shipping Max
    "Direct (FB/IG)": 0.02  # E-Wallet / Bank Payment Gateway Processing Fee (GCash/Maya)
}

st.divider()

# Only calculate if the user fills in Selling Price and Cost
if selling_price and cost_price:
    platform_fee = selling_price * fee_rates[platform]
    total_costs = cost_price + platform_fee + ad_spend + packaging_cost
    net_profit = selling_price - total_costs
    profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0

    st.markdown(f"### 📊 Net Profit Breakdown: **{item_name if item_name else 'Unassigned Item'}**")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Gross Revenue", f"₱{selling_price:,.2f}")
    col_b.metric("Platform Cut", f"₱{platform_fee:,.2f}", delta=f"-{fee_rates[platform]*100:.0f}% Fee", delta_color="inverse")
    col_c.metric("NET PROFIT", f"₱{net_profit:,.2f}", delta=f"{profit_margin:.1f}% Net Margin")

    # Dynamic Intelligence Alerts
    if profit_margin < 15.0 and net_profit > 0:
        st.error("🚨 DANGER: Your profit margin is below 15%! You are one ad-spend spike or price adjustment away from losing money.")
    elif profit_margin >= 30.0:
        st.success("🔥 HIGH PROFIT: Strong margins! You have healthy room for promotions or scaling ad spend.")
    elif net_profit <= 0:
        st.error("❌ CRITICAL LOSS: You are currently SELLING AT A LOSS on this product after all platform cuts!")
    else:
        st.warning("⚠️ MODERATE: Healthy margin, but monitor ad spend closely.")

    st.divider()

    # Goal Planner
    st.subheader("🎯 Monthly Goal & Volume Calculator")
    target_income = st.number_input("How much NET profit do you want to earn monthly? (PHP)", value=15000.0, step=1000.0)

    if net_profit > 0:
        units_needed = int(target_income / net_profit) + 1
        st.info(f"💡 To make **₱{target_income:,.2f}** clear profit on this item, you must sell **{units_needed} units** per month (~{int(units_needed/30) + 1} sales/day).")
    else:
        st.error("Cannot calculate goal volume while net profit per unit is zero or negative.")

else:
    st.info("👆 Please enter a Selling Price and Base Cost (Puhunan) above to view your profit analysis.")

# Professional Footer Disclosure
st.caption("---")
st.caption("ℹ️ *Fee structures are based on standard 2026 marketplace seller center baselines including platform commission, payment gateway processing, and baseline service fees. Real fees may vary slightly depending on individual seller tier programs.*")
