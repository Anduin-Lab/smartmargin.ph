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
st.subheader("Ad-Scale & ROAS Target Engine for PH Sellers")
st.caption("Determine Exact Breakeven ROAS & Maximum Allowable Ad CPA Before Scaling Paid Traffic")

st.divider()

# Input Section
col1, col2 = st.columns(2)

with col1:
    item_name = st.text_input("Product Name", placeholder="e.g. Ergonomic Chair")
    selling_price = st.number_input("Selling Price (PHP)", value=None, placeholder="e.g. 2500.00")
    cost_price = st.number_input("Base Cost / Puhunan (PHP)", value=None, placeholder="e.g. 1100.00")

with col2:
    platform = st.selectbox("Sales Channel", ["Shopee", "TikTok Shop", "Lazada", "Direct (FB/IG)"])
    packaging_cost = st.number_input("Packaging & COGS Extras (PHP)", value=0.0, placeholder="e.g. 50.00")
    current_cpa = st.number_input("Current Ad CPA / Cost per Sale (PHP)", value=0.0, placeholder="e.g. 180.00")

# Fee Rates Logic
fee_rates = {
    "Shopee": 0.12,        
    "TikTok Shop": 0.10,    
    "Lazada": 0.11,        
    "Direct (FB/IG)": 0.02  
}

st.divider()

if selling_price and cost_price:
    platform_fee = selling_price * fee_rates[platform]
    
    # Pre-Ad Margin (Profit before spending a single peso on ads)
    pre_ad_profit = selling_price - (cost_price + platform_fee + packaging_cost)
    
    # Net Profit (After Ad CPA)
    net_profit = pre_ad_profit - current_cpa
    profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0
    
    # ROAS & CPA Intelligence Math
    max_allowable_cpa = pre_ad_profit  # Highest CPA allowed before net profit becomes 0
    breakeven_roas = selling_price / max_allowable_cpa if max_allowable_cpa > 0 else 0
    actual_roas = selling_price / current_cpa if current_cpa > 0 else 0

    st.markdown(f"### 📊 Campaign Performance: **{item_name if item_name else 'Unassigned Item'}**")

    # Metrics Row 1: Net Profits
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Gross Revenue", f"₱{selling_price:,.2f}")
    col_b.metric("Platform Cut", f"₱{platform_fee:,.2f}", delta=f"-{fee_rates[platform]*100:.0f}% Fee", delta_color="inverse")
    col_c.metric("NET PROFIT", f"₱{net_profit:,.2f}", delta=f"{profit_margin:.1f}% Margin")

    st.divider()

    # Metrics Row 2: Ad-Scale Intelligence (The Value Hook!)
    st.subheader("🎯 Ad-Scale & ROAS Thresholds")
    col_x, col_y, col_z = st.columns(3)
    
    col_x.metric("Max Allowable CPA", f"₱{max_allowable_cpa:,.2f}", help="Do NOT spend more than this amount to acquire a customer on Meta/TikTok Ads!")
    col_y.metric("Breakeven ROAS", f"{breakeven_roas:.2f}x", help="Minimum required ROAS in Ads Manager to avoid losing money.")
    
    if current_cpa > 0:
        col_z.metric("Current Campaign ROAS", f"{actual_roas:.2f}x", delta=f"{actual_roas - breakeven_roas:+.2f}x vs BE")

    # Ad Alerts
    if current_cpa > max_allowable_cpa and max_allowable_cpa > 0:
        st.error(f"🚨 AD WARNING: Your current CPA (₱{current_cpa:,.2f}) exceeds your Max Allowable CPA (₱{max_allowable_cpa:,.2f})! You are losing ₱{abs(net_profit):,.2f} on every ad-driven sale!")
    elif current_cpa > 0 and current_cpa <= max_allowable_cpa:
        st.success(f"🔥 SCALABLE: Your ad campaign is profitable! You are keeping ₱{net_profit:,.2f} net profit per acquired customer.")
    elif max_allowable_cpa <= 0:
        st.error("❌ IMPOSSIBLE AD MARGIN: Your base costs and platform cuts exceed your selling price. Ads will instantly lose money.")

else:
    st.info("👆 Enter Selling Price and Base Cost (Puhunan) above to unlock your Ad-Scale & ROAS Thresholds.")

st.caption("---")
st.caption("ℹ️ *SmartMargin PH Ad Engine calculates net breakeven ROAS based on real payout after channel commission, payment processing, and fulfillment costs.*")
