import streamlit as st
from datetime import datetime
from utils import data_manager
from utils import ui

st.set_page_config(page_title="Add Rejection", page_icon="➕", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("➕ Add Customer Rejection")

df = data_manager.load_data()

left, right = st.columns(2)

with left:
    product = st.text_input("Product Name")

    age = st.selectbox(
        "Age Group",
        ["18-25", "26-35", "36-45", "46-60", "60+"]
    )

    city = st.text_input("City")

with right:
    salesperson = st.text_input("Salesperson")

    reason = st.selectbox(
        "Rejection Reason",
        [
            "Too Expensive",
            "Need Discount",
            "Need More Information",
            "Already Using Competitor",
            "Not Interested",
            "Bad Timing",
            "Poor Quality",
            "Other",
        ],
    )

    comments = st.text_area("Comments")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    if st.button("Save Rejection", use_container_width=True):
        # basic validation
        if not product.strip() or not city.strip() or not salesperson.strip():
            st.error("Please fill Product, City and Salesperson.")
        else:
            record = {
                "Product": product.strip(),
                "Age Group": age,
                "City": city.strip(),
                "Salesperson": salesperson.strip(),
                "Reason": reason,
                "Comments": comments.strip(),
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            df, added, dups = data_manager.add_record(record, force=False)
            if not added and dups is not None and len(dups) > 0:
                st.warning("Possible duplicate(s) found:")
                st.dataframe(dups, use_container_width=True, hide_index=True)
                if st.button("Force Save Duplicate", use_container_width=True):
                    df, added2, _ = data_manager.add_record(record, force=True)
                    if added2:
                        st.success("Rejection added (duplicate forced).")
            else:
                st.success("Rejection added successfully!")

with col2:
    uploaded = st.file_uploader("Upload CSV (columns: Product,Age Group,City,Salesperson,Reason,Comments)")
    if uploaded is not None:
        merged, err = data_manager.upload_csv_file(uploaded, merge=True)
        if err:
            st.error(f"Upload failed: {err}")
        else:
            st.success("CSV uploaded and merged.")

    if st.button("Backup CSV", use_container_width=True):
        dst = data_manager.backup_csv()
        if dst:
            st.success(f"Backup created: {dst}")
        else:
            st.info("No data to backup.")

st.divider()

st.subheader("Latest Records")

df = data_manager.load_data()
if df.empty:
    st.info("No records found.")
else:
    st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)