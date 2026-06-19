import streamlit as st
import pandas as pd
from utils import data_manager, ui

st.set_page_config(page_title="Reports — RejectIQ", page_icon="🔵", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

ui.page_header(
    "Reports",
    "Export-ready summaries and statistics",
    icon_svg='<svg width="18" height="18" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
)

df = data_manager.load_data()
if df.empty:
    ui.empty_state("No data available yet.")
    st.stop()

# ── Summary ──────────────────────────────────────────────────────────────────
ui.section_label("Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rejections", len(df))
c2.metric("Products", df["Product"].nunique())
c3.metric("Cities", df["City"].nunique())
c4.metric("Salespersons", df["Salesperson"].nunique())

st.divider()

# ── Filters ──────────────────────────────────────────────────────────────────
ui.section_label("Filters")
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

ui.section_label("Report Data")
st.dataframe(filtered.iloc[::-1], use_container_width=True, hide_index=True)

st.divider()

# ── Quick statistics ──────────────────────────────────────────────────────────
ui.section_label("Quick Statistics")
left, right = st.columns(2)
with left:
    st.markdown("<div class='riq-table-header'>Top Products</div>", unsafe_allow_html=True)
    st.dataframe(
        filtered["Product"].value_counts().reset_index().rename(columns={"index": "Product", "Product": "Count"}),
        hide_index=True, use_container_width=True,
    )
    st.markdown("<div class='riq-table-header' style='margin-top:1rem'>Top Cities</div>", unsafe_allow_html=True)
    st.dataframe(
        filtered["City"].value_counts().reset_index().rename(columns={"index": "City", "City": "Count"}),
        hide_index=True, use_container_width=True,
    )
with right:
    st.markdown("<div class='riq-table-header'>Top Reasons</div>", unsafe_allow_html=True)
    st.dataframe(
        filtered["Reason"].value_counts().reset_index().rename(columns={"index": "Reason", "Reason": "Count"}),
        hide_index=True, use_container_width=True,
    )
    st.markdown("<div class='riq-table-header' style='margin-top:1rem'>Salesperson Activity</div>", unsafe_allow_html=True)
    st.dataframe(
        filtered["Salesperson"].value_counts().reset_index().rename(columns={"index": "Salesperson", "Salesperson": "Entries"}),
        hide_index=True, use_container_width=True,
    )

st.divider()

# ── Weekly / monthly summary ──────────────────────────────────────────────────
ui.section_label("Weekly & Monthly Summary")
try:
    filtered["Date"] = pd.to_datetime(filtered["Date"], errors="coerce")
    weekly = filtered.groupby(pd.Grouper(key="Date", freq="W")).size().reset_index(name="Count")
    monthly = filtered.groupby(pd.Grouper(key="Date", freq="M")).size().reset_index(name="Count")
    w_col, m_col = st.columns(2)
    with w_col:
        st.markdown("<div class='riq-table-header'>Weekly</div>", unsafe_allow_html=True)
        st.dataframe(weekly.tail(12), use_container_width=True, hide_index=True)
    with m_col:
        st.markdown("<div class='riq-table-header'>Monthly</div>", unsafe_allow_html=True)
        st.dataframe(monthly.tail(12), use_container_width=True, hide_index=True)
except Exception:
    st.info("Unable to compute weekly/monthly aggregates.")

st.divider()

# ── Leaderboard ──────────────────────────────────────────────────────────────
ui.section_label("Salesperson Leaderboard")
leader = filtered["Salesperson"].value_counts().reset_index()
leader.columns = ["Salesperson", "Entries"]
st.dataframe(leader, use_container_width=True, hide_index=True)

st.divider()

csv = filtered.to_csv(index=False)
st.download_button(
    label="Download Report (CSV)",
    data=csv,
    file_name="customer_rejection_report.csv",
    mime="text/csv",
    use_container_width=True,
)

st.divider()
st.caption("Customer Rejection Intelligence Platform")