import streamlit as st
import pathlib


def inject_css():
    css_path = pathlib.Path("assets/style.css")
    extra = """
    /* Glassmorphism helpers */
    .glass {
      background: rgba(255,255,255,0.06);
      backdrop-filter: blur(6px);
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.06);
      padding: 12px;
    }
    @media (max-width: 600px) {
      .block-container{ padding-left:12px; padding-right:12px }
    }
    """
    try:
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        st.markdown(f"<style>{extra}</style>", unsafe_allow_html=True)
    except Exception:
        pass


def theme_toggle():
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"

    def _toggle():
        st.session_state["theme"] = "light" if st.session_state["theme"] == "dark" else "dark"

    st.sidebar.markdown("**Theme**")
    st.sidebar.button("Toggle Dark/Light", on_click=_toggle)


def sidebar_info():
    st.sidebar.title("CRi — Navigation")
    st.sidebar.markdown("Use the Streamlit pages menu to switch views.")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Quick actions**")


def kpi(title, value, delta=None, help_text=None):
    txt = f"**{title}**\n\n{value}"
    if delta is not None:
        txt += f"  ({delta})"
    if help_text:
        txt += f"\n\n{help_text}"
    st.markdown(f"<div class='glass'>{txt}</div>", unsafe_allow_html=True)


def download_button_for_plotly(fig, filename="chart.png"):
    try:
        import io
        img_bytes = fig.to_image(format="png")
        st.download_button("📥 Download Chart", data=img_bytes, file_name=filename, mime="image/png")
    except Exception:
        st.info("Download not available for this chart.")
