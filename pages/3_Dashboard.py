import streamlit as st
import plotly.express as px
import pandas as pd
from utils import data_manager, ui

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("📊 Dashboard")

df = data_manager.load_data()
if df.empty:
    st.warning("No data available.")
    st.stop()

# Filters
st.sidebar.header("Filters")
search = st.sidebar.text_input("Search (product / city / salesperson)")
products = st.sidebar.multiselect("Product", sorted(df["Product"].dropna().unique()))
cities = st.sidebar.multiselect("City", sorted(df["City"].dropna().unique()))
reasons = st.sidebar.multiselect("Reason", sorted(df["Reason"].dropna().unique()))
date_range = st.sidebar.date_input("Date range", [])

filtered = df.copy()
if search:
    s = str(search).lower()
    filtered = filtered[filtered.apply(lambda r: s in str(r.get("Product","")).lower() or s in str(r.get("City",""")).lower() or s in str(r.get("Salesperson",""")).lower(), axis=1)]
if products:
    filtered = filtered[filtered["Product"].isin(products)]
if cities:
    filtered = filtered[filtered["City"].isin(cities)]
if reasons:
    filtered = filtered[filtered["Reason"].isin(reasons)]
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered["Date"] = pd.to_datetime(filtered["Date"], errors="coerce")
    filtered = filtered[(filtered["Date"] >= start) & (filtered["Date"] <= end)]

total = len(filtered)
top_product = filtered["Product"].mode()[0] if total > 0 else "-"
top_reason = filtered["Reason"].mode()[0] if total > 0 else "-"
top_city = filtered["City"].mode()[0] if total > 0 else "-"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Rejections", total)
col2.metric("Top Product", top_product)
col3.metric("Top Reason", top_reason)
col4.metric("Cities", filtered["City"].nunique())

st.divider()

left, right = st.columns(2)

with left:
    product_data = filtered["Product"].value_counts().reset_index()
    product_data.columns = ["Product", "Count"]
    fig = px.bar(product_data, x="Product", y="Count", title="Product-wise Rejections", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    ui.download_button_for_plotly(fig, "product_rejections.png")

with right:
    reason_data = filtered["Reason"].value_counts().reset_index()
    reason_data.columns = ["Reason", "Count"]
    fig2 = px.pie(reason_data, names="Reason", values="Count", title="Rejection Reasons")
    st.plotly_chart(fig2, use_container_width=True)
    ui.download_button_for_plotly(fig2, "rejection_reasons.png")

left, right = st.columns(2)

with left:
    city_data = filtered["City"].value_counts().reset_index()
    city_data.columns = ["City", "Count"]
    fig3 = px.bar(city_data, x="City", y="Count", title="City-wise Rejections", text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)
    ui.download_button_for_plotly(fig3, "city_rejections.png")

with right:
    sales_data = filtered["Salesperson"].value_counts().reset_index()
    sales_data.columns = ["Salesperson", "Count"]
    fig4 = px.bar(sales_data, x="Salesperson", y="Count", title="Salesperson Entries", text_auto=True)
    st.plotly_chart(fig4, use_container_width=True)
    ui.download_button_for_plotly(fig4, "salesperson_entries.png")

st.divider()

st.subheader("Daily Rejection Trend & Forecast")
try:
    filtered["Date"] = pd.to_datetime(filtered["Date"], errors="coerce")
    trend = filtered.groupby(filtered["Date"].dt.date).size().reset_index(name="Count")
    trend["Date"] = pd.to_datetime(trend["Date"])
    fig_trend = px.line(trend, x="Date", y="Count", markers=True, title="Rejections Over Time")
    # simple forecast: next 7 days using last 14-day mean
    recent = trend.tail(14)["Count"].mean() if len(trend) > 0 else 0
    import datetime as _dt
    future = []
    last_date = trend["Date"].max() if len(trend) > 0 else pd.to_datetime(_dt.date.today())
    for i in range(1, 8):
        future.append({"Date": last_date + _dt.timedelta(days=i), "Count": recent})
    fut_df = pd.DataFrame(future)
    combined = pd.concat([trend, fut_df], ignore_index=True)
    fig_trend.add_scatter(x=fut_df["Date"], y=fut_df["Count"], mode="lines", name="Forecast", line=dict(dash="dash"))
    st.plotly_chart(fig_trend, use_container_width=True)
    ui.download_button_for_plotly(fig_trend, "rejection_trend.png")
except Exception:
    st.info("Trend chart unavailable.")

st.divider()

st.subheader("Filtered Data")
st.dataframe(filtered.iloc[::-1], use_container_width=True, hide_index=True)