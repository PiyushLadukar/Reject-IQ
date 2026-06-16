import streamlit as st
from utils import ui, data_manager
from utils.auth import login, signup

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:

    st.title("RejectIQ")

    option = st.radio(
        "",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if option == "Signup":

        if st.button("Create Account"):

            if signup(
                username,
                password
            ):
                st.success(
                    "Account Created Successfully!"
                )

            else:
                st.error(
                    "Username Already Exists!"
                )

    else:

        if st.button("Login"):

            if login(
                username,
                password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

    st.stop()    

# PAGE CONFIG
st.set_page_config(
    page_title="Customer Rejection Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

st.markdown(
    """
    <div class='glass' style='padding:24px; margin-bottom:16px'>
    <h1>📊 Customer Rejection Intelligence Platform</h1>
    <h3>Turn Customer Rejections into Business Opportunities</h3>
    <p>Capture customer objections, analyze trends, and make smarter business decisions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# quick KPIs
df = data_manager.load_data()
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='glass'><h3>📦 Products</h3><p>{df['Product'].nunique() if not df.empty else 0}</p></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='glass'><h3>🌍 Cities</h3><p>{df['City'].nunique() if not df.empty else 0}</p></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='glass'><h3>👨‍💼 Sales Team</h3><p>{df['Salesperson'].nunique() if not df.empty else 0}</p></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='glass'><h3>🧠 Insights</h3><p>{'Available' if not df.empty else 'No data'}</p></div>", unsafe_allow_html=True)

st.write("")

left, right = st.columns(2)
with left:
    st.markdown("""
    <div class='glass'>
    <h3>✨ Features</h3>
    <ul>
      <li>Record customer rejections</li>
      <li>Track product performance</li>
      <li>Analyze rejection reasons</li>
      <li>Salesperson analytics</li>
      <li>City-wise trends</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown("""
    <div class='glass'>
    <h3>📈 Workflow</h3>
    <ol>
      <li>Salesperson records rejection</li>
      <li>Data stored in CSV</li>
      <li>Dashboard updates</li>
      <li>AI generates insights</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("How to Use")
st.write("Use the Streamlit Pages menu to navigate: Home, Add Rejection, Dashboard, AI Insights, Reports, Admin.")

st.markdown("---")
st.caption("Customer Rejection Intelligence Platform")