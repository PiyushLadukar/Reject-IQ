import streamlit as st
from utils import data_manager, ui

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("🏠 Home")
st.write("Welcome to the Customer Rejection Intelligence Platform")

df = data_manager.load_data()
total = len(df)

top_product = df["Product"].mode()[0] if total > 0 and not df["Product"].isna().all() else "-"
top_reason = df["Reason"].mode()[0] if total > 0 and not df["Reason"].isna().all() else "-"
top_city = df["City"].mode()[0] if total > 0 and not df["City"].isna().all() else "-"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rejections", total)
c2.metric("Top Product", top_product)
c3.metric("Top Reason", top_reason)
c4.metric("Top City", top_city)

st.divider()

left, right = st.columns([2, 1])
with left:
    st.subheader("Recent Entries")
    if total > 0:
        st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("No data available.")
with right:
    st.subheader("Quick Summary")
    st.success(f"📦 Products : {df['Product'].nunique() if total > 0 else 0}")
    st.success(f"🌍 Cities : {df['City'].nunique() if total > 0 else 0}")
    st.success(f"👨‍💼 Salespersons : {df['Salesperson'].nunique() if total > 0 else 0}")
    st.success(f"❌ Rejection Reasons : {df['Reason'].nunique() if total > 0 else 0}")

st.divider()

st.subheader("Platform Features")
a, b, c = st.columns(3)
with a:
    st.info("➕ Add Rejections — Store customer feedback.")
with b:
    st.info("📊 Dashboard — View rejection trends.")
with c:
    st.info("🧠 AI Insights — Get smart recommendations.")

st.divider()
st.caption("Customer Rejection Intelligence Platform")