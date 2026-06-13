import streamlit as st
from utils import data_manager, insights, ui
import pandas as pd

st.set_page_config(page_title="AI Insights", page_icon="🧠", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("🧠 AI Insights")

df = data_manager.load_data()
if df.empty:
    st.warning("No data found.")
    st.stop()

st.subheader("Overall Summary")
total = len(df)
top_product = df["Product"].mode()[0] if total > 0 else "-"
top_reason = df["Reason"].mode()[0] if total > 0 else "-"
top_city = df["City"].mode()[0] if total > 0 else "-"
top_salesperson = df["Salesperson"].mode()[0] if total > 0 else "-"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", total)
c2.metric("Top Product", top_product)
c3.metric("Top Reason", top_reason)
c4.metric("Top City", top_city)

st.divider()

st.subheader("Product Insights & Opportunity Score")
product_counts = df["Product"].value_counts()
for product in product_counts.index:
    temp = df[df["Product"] == product]
    reason = temp["Reason"].mode()[0]
    city = temp["City"].mode()[0]
    opportunity = max(0, 100 - int((len(temp) / len(df)) * 100))
    st.info(f"### 📦 {product}\nMost Common Reason: **{reason}**\nMost Affected City: **{city}**\nTotal Rejections: **{len(temp)}**\nOpportunity Score: **{opportunity}/100**")
    # simple rule-based suggestions
    if reason == "Too Expensive":
        st.success("Suggestion: Consider discounts or budget variants.")
    elif reason == "Already Using Competitor":
        st.success("Suggestion: Highlight unique features and benefits.")
    elif reason == "Need Discount":
        st.success("Suggestion: Launch promotional offers.")
    elif reason == "Need More Information":
        st.success("Suggestion: Improve product demonstrations.")
    elif reason == "Not Interested":
        st.success("Suggestion: Improve targeting and marketing.")
    else:
        st.success("Suggestion: Collect additional customer feedback.")

st.divider()

st.subheader("City Insights")
city_counts = df["City"].value_counts()
for city in city_counts.index:
    temp = df[df["City"] == city]
    reason = temp["Reason"].mode()[0]
    st.warning(f"🌍 {city}\nMain rejection reason: {reason}\nTotal rejections: {len(temp)}")

st.divider()

st.subheader("Salesperson Activity")
sales = df["Salesperson"].value_counts().reset_index()
sales.columns = ["Salesperson", "Entries"]
st.dataframe(sales, use_container_width=True, hide_index=True)

st.divider()

st.subheader("Quick Recommendations")
for item in insights.get_all_insights(df):
    st.success(item)

st.divider()

st.subheader("Business Health Score")
score = 100
if total > 50:
    score -= 10
if top_reason == "Too Expensive":
    score -= 15
if top_reason == "Already Using Competitor":
    score -= 10
if top_reason == "Need Discount":
    score -= 8
if score >= 80:
    st.success(f"Business Health Score : {score}/100")
elif score >= 60:
    st.warning(f"Business Health Score : {score}/100")
else:
    st.error(f"Business Health Score : {score}/100")

st.divider()

st.subheader("Customer Segmentation (Simple)")
seg = []
seg.append(("At-risk", df[df["Reason"].isin(["Too Expensive","Need Discount"])].shape[0]))
seg.append(("Needs Info", df[df["Reason"]=="Need More Information"].shape[0]))
seg.append(("Competitor", df[df["Reason"]=="Already Using Competitor"].shape[0]))
for name, count in seg:
    st.info(f"{name}: {count}")