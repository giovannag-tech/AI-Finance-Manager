import streamlit as st


def aplicar_estilo():
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f7f2ff 0%, #ffffff 60%);
        }

        [data-testid="stSidebar"] {
            background-color: #eee7ff;
        }

        h1 {
            color: #3b1c73;
            font-weight: 800;
        }

        h2, h3 {
            color: #4b2e83;
        }

        [data-testid="stMetric"] {
            background-color: white;
            padding: 22px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(60, 30, 120, 0.12);
            border: 1px solid #eadfff;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 700;
            border: 1px solid #7c3aed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )