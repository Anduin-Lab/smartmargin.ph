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
st.subheader("TikTok Shop & E-Com Margin Intelligence Engine")
st.caption("Expose Hidden Platform Cuts, Ad CPA Limits, & Real Take-Home Cash Flow")

st.divider()

# Input Section
col1, col2 = st.columns(2)

with col1:
    item_name = st.text_input("Product Name", placeholder="e.g. Viral Lip Gloss / Tech Gadget")
    selling_price = st.number_input("Selling Price (PHP)", value=None, placeholder="e.g. 499.00")
    cost_price = st.number_input("Base Cost / Puhunan (PHP)", value=None, placeholder="e.g. 180.00")

with col2:
    platform = st.selectbox("Sales Channel", ["TikTok Shop", "Shopee", "Lazada", "Direct (FB/IG)"])
    
    # Dynamic Fee Percentage Selector (Gives total user accuracy!)
    if platform == "TikTok Shop":
        fee_pct = st.slider("TikTok Total Cut % (Commission + Gateway)", min_value=4.0, max_value=12.0, value=8.0, step=0.5) / 100
    elif platform == "Shopee":
        fee_pct = st.slider("Shopee Total Cut % (Commission + Transaction + Service)", min_value=6.0, max_value=18.0, value=12.0, step=0.5) / 100
    elif platform == "Lazada":
        fee_pct = st.slider("Lazada Total Cut %", min_value=5.0, max_value=15.0, value=11.0, step=0.5) / 100
    else:
        fee_pct = 0.02  # Direct Sales GCash/Maya

    packaging_cost = st.number_input("Packaging & COGS Extras (PHP)", value=0.0, placeholder="e.g. 15.00")
    current_cpa = st.number_input("Est. Ad CPA or Affiliate Comm. (PHP)", value=0.0, placeholder="e.g. 80.00")

st.divider()

if selling_price and cost_price:
    platform_fee = selling_price * fee_pct
    pre_ad_profit = selling_price - (cost_price + platform_fee + packaging_cost)
    net_profit = pre_ad_profit - current_cpa
    profit_margin = (net_profit / selling_price) * 100 if selling_price > 0 else 0
    
    # Advanced Metrics
    max_allowable_cpa = pre_ad_profit
    breakeven_roas = selling_price / max_allowable_cpa if max_allowable_cpa > 0 else 0
    loss_per_100_sales = (platform_fee + packaging_cost + current_cpa) * 100

    st.markdown(f"### 📊 Margin Analysis: **{item_name if item_name else 'Unassigned Product'}**")

    # Primary Metrics
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Gross Revenue", f"₱{selling_price:,.2f}")
    col_b.metric("Platform Cut", f"₱{platform_fee:,.2f}", delta=f"-{fee_pct*100:.1f}% Cut", delta_color="inverse")
    col_c.metric("NET PROFIT", f"₱{net_profit:,.2f}", delta=f"{profit_margin:.1f}% Margin")

    st.divider()

    # Ad & Scale Intelligence Card
    st.subheader("🎯 TikTok Ad & Affiliate Guardrails")
    col_x, col_y, col_z = st.columns(3)
    
    col_x.metric("Max Allowable CPA", f"₱{max_allowable_cpa:,.2f}", help="Do NOT pay more than this per sale to TikTok Ads or Affiliates!")
    col_y.metric("Breakeven ROAS", f"{breakeven_roas:.2f}x", help="Minimum required ROAS in TikTok Ads Manager to avoid losing money.")
    col_z.metric("Fulfillment Drain / 100 Orders", f"₱{loss_per_100_sales:,.2f}", help="Total cash going to platform, packaging, and ads for every 100 units.")

    # Status Alerts
    if net_profit <= 0:
        st.error("❌ CRITICAL DANGER: You are SELLING AT A LOSS on this item after platform cuts and acquisition costs!")
    elif profit_margin < 15.0:
        st.warning("⚠️ THIN MARGIN: Your profit margin is below 15%. One ad-cost bump will wipe out your profit.")
    else:
        st.success(f"🔥 HIGHLY PROFITABLE: You are keeping **₱{net_profit:,.2f}** net profit per sale!")

else:
    st.info("👆 Input Selling Price and Base Cost (Puhunan) above to reveal your margins.")

st.caption("---")
st.caption("⚡ *SmartMargin PH Engine | Built for Local E-Commerce Founders*")
