import streamlit as st
from utils import data_manager, ui
import pandas as pd

st.set_page_config(page_title="Admin", page_icon="🔧", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.title("🔧 Admin — Manage Records & Backups")

df = data_manager.load_data()
if df.empty:
    st.info("No records to manage.")

st.subheader("Records")
selected = st.selectbox("Select record ID to edit/delete", [None] + (df["ID"].astype(str).tolist() if not df.empty else []))
if selected:
    rid = int(selected)
    rec = df[df["ID"] == rid].iloc[0].to_dict()
    with st.form("edit_form"):
        product = st.text_input("Product", value=rec.get("Product", ""))
        age = st.text_input("Age Group", value=rec.get("Age Group", ""))
        city = st.text_input("City", value=rec.get("City", ""))
        salesperson = st.text_input("Salesperson", value=rec.get("Salesperson", ""))
        reason = st.text_input("Reason", value=rec.get("Reason", ""))
        comments = st.text_area("Comments", value=rec.get("Comments", ""))
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            updates = {
                "Product": product,
                "Age Group": age,
                "City": city,
                "Salesperson": salesperson,
                "Reason": reason,
                "Comments": comments,
            }
            df2, ok = data_manager.edit_record(rid, updates)
            if ok:
                st.success("Record updated.")
            else:
                st.error("Unable to update record.")

    if st.button("Delete Record"):
        _, ok = data_manager.delete_record(rid)
        if ok:
            st.success("Record deleted.")
        else:
            st.error("Delete failed.")

st.divider()

st.subheader("Backups")
if st.button("Create Backup"):
    dst = data_manager.backup_csv()
    if dst:
        st.success(f"Backup created: {dst}")
    else:
        st.info("No data to backup.")

backups = data_manager.list_backups()
if backups:
    sel = st.selectbox("Available backups", backups)
    if st.button("Restore Selected Backup"):
        ok = data_manager.restore_backup(sel)
        if ok:
            st.success("Backup restored. Reload the app to see changes.")
        else:
            st.error("Restore failed.")
else:
    st.info("No backups found.")

st.divider()
st.subheader("All Records")
st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
