import streamlit as st


def show_login(validate_user, register_user):

    st.markdown("""
    <style>

    /* =========================
       PAGE
    ========================= */

    .stApp{
        background:#EEF2F7;
    }

    [data-testid="stSidebar"]{
        display:none;
    }

    header{
        visibility:hidden;
    }

    /* =========================
       FONT & TEXT
    ========================= */

    html, body, [class*="css"] {
        font-family: "Poppins", sans-serif;
    }

    .logo{
        text-align:center;
        font-size:34px;
        font-weight:700;
        color:#111827;
        margin-bottom:20px;
    }

    .title{
        text-align:center;
        font-size:42px;
        font-weight:800;
        color:#0F172A;
        margin-bottom:10px;
    }

    .subtitle{
        text-align:center;
        font-size:17px;
        color:#475569;
        margin-bottom:30px;
        font-weight:500;
    }

    /* =========================
       CARD
    ========================= */

    .login-card{
        background:white;
        padding:40px;
        border-radius:24px;
        box-shadow:0px 15px 45px rgba(0,0,0,0.08);
    }

    /* =========================
       INPUTS
    ========================= */

    .stTextInput label{
        color:#111827 !important;
        font-size:16px !important;
        font-weight:600 !important;
    }

    .stTextInput input{
        border-radius:14px !important;
        height:55px !important;
        border:1px solid #CBD5E1 !important;
        background-color:white !important;
        color:#111827 !important;
        font-size:16px !important;
    }
    .stTextInput input::placeholder{
        color:#94A3B8 !important;
        opacity:1 !important;
    }

    /* =========================
       SEGMENTED CONTROL
    ========================= */

    div[data-baseweb="tab-list"]{
        width:100% !important;
        display:flex !important;
        gap:8px !important;
        margin-bottom:25px !important;
    }

    div[data-baseweb="tab"]{
        flex:1 !important;
        justify-content:center !important;
        font-size:16px !important;
        font-weight:700 !important;
        padding:14px !important;
        border-radius:12px !important;
    }

    /* =========================
       BUTTON
    ========================= */

    .stButton button{
        width:100%;
        height:55px;
        border-radius:14px;
        border:none;
        font-size:17px;
        font-weight:700;
        background:#64748B;
        color:white;
    }

    .stButton button:hover{
        background:#475569;
    }

    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        st.markdown(
            """
            <div class="logo">
                 Smart Tourism Analytics
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="title">
                Welcome
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="subtitle">
                Plan smarter journeys with AI-powered travel insights.
            </div>
            """,
            unsafe_allow_html=True
        )

        option = st.segmented_control(
            "Account",
            ["Login", "Register"],
            default="Login"
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        st.write("")

        if option == "Login":

            if st.button("Sign In"):

                if validate_user(username, password):

                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.rerun()

                else:
                    st.error("Invalid username or password")

        else:

            if st.button("Create Account"):

                if register_user(username, password):

                    st.success(
                        "Registered successfully! Now login."
                    )

                else:
                    st.warning(
                        "Username already exists"
                    )

    st.stop()