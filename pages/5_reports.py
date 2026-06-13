import streamlit as st
import pandas as pd
from utils import data_manager, ui

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("📄 Reports")

df = data_manager.load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

st.subheader("Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rejections", len(df))
c2.metric("Products", df["Product"].nunique())
c3.metric("Cities", df["City"].nunique())
c4.metric("Salespersons", df["Salesperson"].nunique())

st.divider()

st.subheader("Filters")
col1, col2, col3 = st.columns(3)
with col1:
    product = st.selectbox("Product", ["All"] + sorted(df["Product"].dropna().unique().tolist()))
with col2:
    city = st.selectbox("City", ["All"] + sorted(df["City"].dropna().unique().tolist()))
with col3:
    reason = st.selectbox("Reason", ["All"] + sorted(df["Reason"].dropna().unique().tolist()))

filtered = df.copy()
if product != "All":
    filtered = filtered[filtered["Product"] == product]
if city != "All":
    filtered = filtered[filtered["City"] == city]
if reason != "All":
    filtered = filtered[filtered["Reason"] == reason]

st.divider()

st.subheader("Report Data")
st.dataframe(filtered.iloc[::-1], use_container_width=True, hide_index=True)

st.divider()

st.subheader("Quick Statistics")
left, right = st.columns(2)
with left:
    st.write("### Top Products")
    st.dataframe(filtered["Product"].value_counts().reset_index().rename(columns={"index":"Product","Product":"Count"}), hide_index=True, use_container_width=True)
    st.write("### Top Cities")
    st.dataframe(filtered["City"].value_counts().reset_index().rename(columns={"index":"City","City":"Count"}), hide_index=True, use_container_width=True)
with right:
    st.write("### Top Reasons")
    st.dataframe(filtered["Reason"].value_counts().reset_index().rename(columns={"index":"Reason","Reason":"Count"}), hide_index=True, use_container_width=True)
    st.write("### Salesperson Activity")
    st.dataframe(filtered["Salesperson"].value_counts().reset_index().rename(columns={"index":"Salesperson","Salesperson":"Entries"}), hide_index=True, use_container_width=True)

st.divider()

# Weekly and Monthly reports
st.subheader("Weekly & Monthly Summary")
try:
    filtered["Date"] = pd.to_datetime(filtered["Date"], errors="coerce")
    weekly = filtered.groupby(pd.Grouper(key="Date", freq="W")).size().reset_index(name="Count")
    monthly = filtered.groupby(pd.Grouper(key="Date", freq="M")).size().reset_index(name="Count")
    st.write("### Weekly")
    st.dataframe(weekly.tail(12), use_container_width=True, hide_index=True)
    st.write("### Monthly")
    st.dataframe(monthly.tail(12), use_container_width=True, hide_index=True)
except Exception:
    st.info("Unable to compute weekly/monthly aggregates.")

st.divider()

# Leaderboard
st.subheader("Salesperson Leaderboard")
leader = filtered["Salesperson"].value_counts().reset_index()
leader.columns = ["Salesperson", "Entries"]
st.dataframe(leader, use_container_width=True, hide_index=True)

st.divider()

csv = filtered.to_csv(index=False)
st.download_button(label="📥 Download Report", data=csv, file_name="customer_rejection_report.csv", mime="text/csv", use_container_width=True)

st.divider()
st.caption("Customer Rejection Intelligence Platform")