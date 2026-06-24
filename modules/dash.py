import streamlit as st
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

tourism_df = pd.read_csv(
    os.path.join(BASE_DIR, "tourism.csv")
)

attraction_df = pd.read_csv(
    os.path.join(BASE_DIR, "cleaned_data_India.csv"),
    low_memory=False
)
def show_dashboard():

    # =========================
    # CSS
    # =========================
    st.markdown("""
    <style>

    .stApp{
        background:#EEF2F7;
    }

    .hero{
        background:linear-gradient(135deg,#CBD5E1,#E2E8F0);
        padding:40px;
        border-radius:25px;
        text-align:center;
        color:#0F172A;
        margin-bottom:25px;
    }

    .section-card{
        padding:25px;
        border-radius:20px;
        color:#0F172A;
        min-height:160px;
        box-shadow:0px 6px 15px rgba(0,0,0,0.05);
    }

    .map-card{
        background:#DBEAFE;
    }

    .heat-card{
        background:#FCE7F3;
    }

    .trend-card{
        background:#DDD6FE;
    }

    .budget-card{
        background:#FEF3C7;
    }

    .predict-card{
        background:#CFFAFE;
    }

    .service-card{
        background:white;
        padding:20px;
        border-radius:18px;
        text-align:center;
        box-shadow:0px 4px 12px rgba(0,0,0,0.05);
        color:#0F172A;
    }

    .service-card h3{
        margin-bottom:10px;
    }
     h1,h2,h3,h4,h5,h6,p,label,span{
        color:#1E293B !important;
    }

    [data-testid="stMetricValue"]{
        color:#1E293B !important;
    }

    [data-testid="stMetricLabel"]{
        color:#475569 !important;
    }

    [data-testid="stMetricDelta"]{
        color:#16A34A !important;
    }

    .stMarkdown{
        color:#1E293B !important;
    } 
    [data-testid="metric-container"]{
        background:white;
        border-radius:18px;
        padding:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.05);
    }
    .stButton > button {
        background-color: #DDD6FE !important;
        color: #1E293B !important;
        border: 1px solid #A5B4FC !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        height: 55px !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background-color: #A5B4FC !important;
        color: #0F172A !important;
        border: 1px solid #818CF8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HERO BANNER
    # =========================
    st.markdown("""
    <div class="hero">
        <h1>🌍 Smart Tourism Analytics Platform</h1>
        <h4>Travel Intelligence • Prediction • Optimization • Discovery</h4>
        <p>Plan smarter journeys using AI-powered tourism insights</p>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # KPI CARDS
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🌍 Destinations",
            tourism_df["name"].nunique()
        )

    with col2:
        st.metric(
            "🏨 Countries",
            tourism_df["country"].nunique()
        )

    with col3:
        st.metric(
            "🏝 Categories",
            tourism_df["category"].nunique()
        )

    with col4:
        st.metric(
            "⭐ Avg Rating",
            round(tourism_df["rating"].mean(), 2)
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # MAP + HEATMAP
    # =========================
    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🗺 Interactive Tourist Map")

        country_counts = (
            tourism_df["country"]
            .value_counts()
            .reset_index()
        )

        country_counts.columns = [
            "country",
            "destinations"
        ]

        fig = px.choropleth(
            country_counts,
            locations="country",
            locationmode="country names",
            color="destinations",
            hover_name="country",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            paper_bgcolor="#EEF2F7",
            plot_bgcolor="#EEF2F7",

            font=dict(
                color="#334155",
                size=14
            ),

            title_font=dict(
                color="#1E293B",
                size=20
            ),

            geo=dict(
                bgcolor="#EEF2F7"
            ),

            margin=dict(
                l=0,
                r=0,
                t=30,
                b=0
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("### 🔥 Tourist Density Analysis")

        city_counts = (
            attraction_df["city"]
            .value_counts()
            .head(15)
        )

        fig = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation="h",
            color=city_counts.values,
            color_continuous_scale="Purples"
        )

        fig.update_layout(
            paper_bgcolor="#EEF2F7",
            plot_bgcolor="#EEF2F7",

            font=dict(
                color="#334155",
                size=14
            ),

            title_font=dict(
                color="#1E293B",
                size=20
            ),

            xaxis=dict(
                title_font=dict(color="#1E293B"),
                tickfont=dict(color="#334155")
            ),

            yaxis=dict(
                title_font=dict(color="#1E293B"),
                tickfont=dict(color="#334155")
            ),

            margin=dict(
                l=0,
                r=0,
                t=30,
                b=0
            )
        )

        st.plotly_chart(
           fig,
           use_container_width=True
        )
    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # ANALYTICS
    # =========================
    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📈 Destination Categories")

        category_counts = (
            tourism_df["category"]
            .value_counts()
            .head(10)
        )

        fig = px.bar(
           x=category_counts.index,
           y=category_counts.values,
           color=category_counts.values,
           title="Top Destination Categories",
           color_continuous_scale=[
              "#94A3B8",
              "#A5B4FC",
              "#C4B5FD",
              "#F9A8D4"
            ]
        )

        fig.update_layout(
           paper_bgcolor="#EEF2F7",
           plot_bgcolor="#EEF2F7",

           font=dict(
             color="#334155",
             size=14
            ),

        title_font=dict(
           color="#1E293B",
           size=20
            ),

        xaxis=dict(
            tickfont=dict(color="#475569")
            ),

        yaxis=dict(
            tickfont=dict(color="#475569")
            ),

        coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("### 🌦 Climate Distribution")

        climate_counts = (
            tourism_df["climate"]
            .value_counts()
        )

        fig = px.pie(
            values=climate_counts.values,
            names=climate_counts.index,
            hole=0.45,  # donut chart
            color_discrete_sequence=[
                "#94A3B8",
                "#A5B4FC",
                "#C4B5FD",
                "#F9A8D4",
                "#FCD34D"
            ]
        )

        fig.update_layout(
            paper_bgcolor="#EEF2F7",

            font=dict(
                color="#334155",
                size=14
            ),

            legend=dict(
                font=dict(
                     color="#334155",
                     size=13
                )
            ),

            margin=dict(
                l=0,
                r=0,
                t=20,
                b=0
            )
       )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # PREDICTIVE ANALYTICS
    # =========================
    st.markdown("### 🏆 Top Rated Destinations")

    top_dest = tourism_df[
        ["name", "country", "rating"]
    ].sort_values(
        by="rating",
        ascending=False
     ).head(10)

    st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:18px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.05);
        ">
        """, unsafe_allow_html=True)

    styled_df = top_dest.style \
        .set_properties(**{
            'background-color': '#F8FAFC',
            'color': '#1E293B',
            'border-color': '#CBD5E1'
        }) \
        .set_table_styles([
            {
                'selector': 'th',
                'props': [
                    ('background-color', '#DDD6FE'),
                    ('color', '#1E293B'),
                    ('font-weight', 'bold')
                ]
            }
        ])

    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # =========================
    # SERVICES HUB
    # =========================
    st.markdown("## 🚀 Smart Tourism Services")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖 AI Assistant"):
           st.session_state.menu = "AI Travel Planner"
           st.rerun()

    with col2:
        if st.button("🚗 Route Optimizer"):
           st.session_state.menu = "Route Optimizer"
           st.rerun()

    with col3:
        if st.button("🌦 Weather Forecast"):
           st.session_state.menu = "Weather Forecast"
           st.rerun()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏨 Hotel Recommendation"):
           st.session_state.menu = "Hotel Recommendation"
           st.rerun()

    with col2:
        if st.button("🏝 Destination Recommendation"):
           st.session_state.menu = "Destination Recommendation"
           st.rerun()

    with col3:
        if st.button("💸 Cost Prediction"):
           st.session_state.menu = "Cost Prediction"
           st.rerun()