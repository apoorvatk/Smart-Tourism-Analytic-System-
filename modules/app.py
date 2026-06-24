
import sys
import os
import streamlit as st
import warnings
import pandas as pd

import route_optimize
import tourist_recommend
import dest_recommendation
from dash import show_dashboard
from login import show_login

warnings.filterwarnings("ignore")

# =========================
# USERS SYSTEM
# =========================
USERS_FILE = "users.csv"


def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USERS_FILE, index=False)

    return pd.read_csv(USERS_FILE)


def validate_user(username, password):
    df = load_users()
    user = df[(df["username"] == username) & (df["password"] == password)]
    return not user.empty


def register_user(username, password):
    df = load_users()

    if username in df["username"].values:
        return False

    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USERS_FILE, index=False)

    return True


# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(page_title="Smart Tourism Platform", layout="wide")
st.markdown("""
<style>

/* =========================
   SIDEBAR
========================= */

[data-testid="stSidebar"]{
    background:#E2E8F0;
    border-right:1px solid #CBD5E1;
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:#1E293B !important;
}

/* Selectbox */
[data-testid="stSidebar"] .stSelectbox div{
    color:#1E293B !important;
}

/* Logout button */
[data-testid="stSidebar"] .stButton button{
    background:#94A3B8;
    color:#0F172A;
    border:none;
    border-radius:12px;
    font-weight:600;
}

[data-testid="stSidebar"] .stButton button:hover{
    background:#CBD5E1;
}

/* Welcome user */
/* Sidebar Background */
[data-testid="stSidebar"]{
    background:#CBD5E1 !important;
}

/* All Sidebar Text */
[data-testid="stSidebar"] *{
    color:#1E293B !important;
}

/* Welcome User Card */
.sidebar-user{
    background:#E2E8F0;
    padding:15px;
    border-radius:15px;
    text-align:center;
    margin-bottom:15px;
    color:#1E293B !important;
}

/* Sidebar Selectbox */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div{
    background:#E2E8F0 !important;
    color:#1E293B !important;
    border-radius:10px !important;
}

/* Dropdown Menu */
[data-baseweb="popover"] *{
    color:#1E293B !important;
    background:white !important;
}

/* Logout Button */
[data-testid="stSidebar"] .stButton > button{
    background:#DDD6FE !important;
    color:#1E293B !important;
    border:1px solid #A5B4FC !important;
    border-radius:12px !important;
    font-weight:600 !important;
}

[data-testid="stSidebar"] .stButton > button:hover{
    background:#C4B5FD !important;
    color:#0F172A !important;
}

</style>
""", unsafe_allow_html=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# =========================
# SESSION STATE INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# =========================
# LOAD MODULES
# =========================
@st.cache_resource
def load_modules():
    import curr_converter as currency
    import weather
    import cost_prediction
    import hotel_recommend
    import tourist_recommend
    import dest_recommendation
    return currency, weather, cost_prediction, hotel_recommend, tourist_recommend, dest_recommendation


@st.cache_resource
def load_ai_module():
    import ai_assisstant
    return ai_assisstant


currency, weather, cost_prediction, hotel_recommend, tourist_recommend, dest_recommendation = load_modules()
travel_ai = load_ai_module()


# =========================
# LOGIN PAGE
# =========================
if not st.session_state.logged_in:
    show_login(
        validate_user,
        register_user
    )

# =========================
# SIDEBAR (AFTER LOGIN ONLY)
# =========================
if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"
st.sidebar.markdown(
    f"""
    <div class="sidebar-user">
        👤 Welcome<br>
        <b>{st.session_state.user}</b>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Dashboard",
        "AI Travel Planner",
        "Currency Converter",
        "Weather Forecast",
        "Cost Prediction",
        "Hotel Recommendation",
        "Tourist Attractions",
        "Route Optimizer",
        "Destination Recommendation"
    ],
    index=[
        "Dashboard",
        "AI Travel Planner",
        "Currency Converter",
        "Weather Forecast",
        "Cost Prediction",
        "Hotel Recommendation",
        "Tourist Attractions",
        "Route Optimizer",
        "Destination Recommendation"
    ].index(st.session_state.menu)
)

st.session_state.menu = menu

if menu == "Dashboard":
    show_dashboard()



elif menu == "AI Travel Planner":

    st.subheader("AI Travel Itinerary Generator")

    query = st.text_input("Enter destination or travel idea")

    if st.button("Generate Plan"):

        if query.strip():

            with st.spinner("Generating your travel plan..."):
                plan = travel_ai.get_travel_plan(query)

            st.markdown(plan)

        else:
            st.warning("Enter a valid query")



elif menu == "Currency Converter":

    st.subheader("💱 Live Currency Converter")

    currencies = ["USD","INR","EUR","GBP","JPY","AUD","CAD","CHF","CNY","SGD","AED","NZD"]

    col1, col2, col3 = st.columns(3)

    with col1:
        from_currency = st.selectbox("From Currency", currencies, index=0)

    with col2:
        to_currency = st.selectbox("To Currency", currencies, index=1)

    with col3:
        amount = st.number_input("Amount", min_value=0.01, value=1.00, step=0.01)

    if st.button("Convert Currency"):

        with st.spinner("Converting..."):
            result = currency.convert_currency(from_currency, to_currency, amount)

        if result is None:
            st.error("Conversion failed.")
        else:
            st.success(f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}")



elif menu == "Weather Forecast":

    st.subheader("Check Weather")

    city = st.text_input("Enter City")

    if st.button("Get Weather"):

        if city.strip():

            with st.spinner("Fetching weather..."):
                data = weather.get_weather(city)

            if data:
                st.json(data)
            else:
                st.error("Could not fetch weather")

        else:
            st.warning("Enter a city name")

    st.markdown("---")

    st.subheader("Forecast")

    city2 = st.text_input("City for Forecast")
    date = st.text_input("Date (YYYY-MM-DD)")

    if st.button("Get Forecast"):

        if city2 and date:

            result = weather.get_weather_for_travel_date(city2, date)

            if result is not None:
                st.dataframe(result)
            else:
                st.warning("No forecast data found")

        else:
            st.warning("Fill all fields")



elif menu == "Cost Prediction":

    st.subheader("💰 Trip Cost Prediction")

    col1, col2 = st.columns(2)

    with col1:
        lead_time = st.number_input("Lead Time", min_value=0, value=30)
        adults = st.number_input("Adults", min_value=1, value=2)
        children = st.number_input("Children", min_value=0, value=0)
        babies = st.number_input("Babies", min_value=0, value=0)
        total_nights = st.number_input("Total Nights", min_value=1, value=3)

    with col2:
        booking_changes = st.number_input("Booking Changes", min_value=0, value=0)
        repeated_guest = st.selectbox("Repeated Guest", [0, 1])

        meal = st.selectbox("Meal", cost_prediction.MEAL_OPTIONS)
        market_segment = st.selectbox("Market Segment", cost_prediction.MARKET_OPTIONS)
        customer_type = st.selectbox("Customer Type", cost_prediction.CUSTOMER_OPTIONS)

    if st.button("Predict Cost"):

        result = cost_prediction.predict_trip_cost(
            lead_time,
            adults,
            children,
            babies,
            meal,
            market_segment,
            customer_type,
            total_nights,
            repeated_guest,
            booking_changes
        )

        if result is not None:
            st.success(f"Estimated Trip Cost: ₹ {result:,.2f}")
        else:
            st.error("Could not predict trip cost.")


elif menu == "Hotel Recommendation":

    st.subheader("🏨 Smart Hotel Recommendation System")


    st.markdown("### 🔍 Find Similar Hotels")

    hotels = hotel_recommend.get_hotels()

    if hotels:

        selected_hotel = st.selectbox("Choose a hotel", hotels)

        if st.button("Get Similar Hotels"):

            with st.spinner("Finding similar hotels..."):

                result = hotel_recommend.recommend_hotel(selected_hotel)

            if result is not None and not result.empty:
                st.success("Similar Hotels Found 👇")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("No similar hotels found.")

    else:
        st.error("No hotel data available.")

    st.markdown("---")



    st.markdown("### 🌍 Find Hotels by City")

    city_input = st.text_input("Enter city name (e.g. Goa, Delhi, Mumbai)")

    if st.button("Get Hotels in City"):

        if city_input.strip():

            with st.spinner("Searching hotels..."):

                result = hotel_recommend.recommend_hotels_by_city(city_input.strip())

            if result is not None and not result.empty:
                st.success(f"Hotels in {city_input} 👇")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("No hotels found for this city.")

        else:
            st.warning("Please enter a city name.")



elif menu == "Tourist Attractions":

    st.subheader("🏛 Tourist Attraction Recommendation System")



    st.markdown("### 🌍 Top Attractions By City")

    city = st.text_input(
        "Enter City Name",
        key="attraction_city"
    )

    if st.button("Get Attractions"):

        result = tourist_recommend.recommend_by_city(city)

        if not result.empty:
            st.dataframe(
                result,
                use_container_width=True
            )
        else:
            st.warning("No attractions found.")

    st.markdown("---")



    st.markdown("### 🎯 Attractions By Category")

    col1, col2 = st.columns(2)

    with col1:
        city2 = st.text_input(
            "City",
            key="city_category"
        )

    with col2:
        category = st.selectbox(
            "Category",
            tourist_recommend.get_categories()
        )

    if st.button("Search Category Attractions"):

        result = tourist_recommend.recommend_by_city_category(
            city2,
            category
        )

        if not result.empty:
            st.dataframe(
                result,
                use_container_width=True
            )
        else:
            st.warning("No attractions found.")

    st.markdown("---")

  

    st.markdown("### 🔍 Similar Attractions")

    attraction = st.selectbox(
        "Select Attraction",
        tourist_recommend.get_attractions()
    )

    if st.button("Recommend Similar Attractions"):

        result = tourist_recommend.recommend_similar_attraction(
            attraction
        )

        if not result.empty:
            st.dataframe(
                result,
                use_container_width=True
            )
        else:
            st.warning("No recommendations found.")
elif menu == "Route Optimizer":

    st.subheader("Route Optimization")

    start_city = st.text_input("Enter Source City")

    end_city = st.text_input("Enter Destination City")

    if st.button("Find Route"):

        if start_city and end_city:

            with st.spinner("Finding best route..."):

                result = route_optimize.get_route_details(
                    start_city,
                    end_city
                )

            if result:

                distance = result["distance"]
                duration = result["duration"]
                roads = result["roads"]

                hours = int(duration // 60)
                minutes = int(duration % 60)

                st.success("Route Found")

                st.markdown("### 🚗 Recommended Route")

                st.write(f"**Start:** {start_city}")

                for road in roads[:15]:
                    st.write("⬇")
                    st.write(f"🛣 {road}")

                st.write("⬇")
                st.write(f"**Destination:** {end_city}")

                st.markdown("### 📊 Travel Details")

                st.write(f"Distance: {distance:.2f} km")
                st.write(f"Travel Time: {hours} hr {minutes} min")

            else:
                st.error("Route not found")

        else:
            st.warning("Please enter both cities")

elif menu == "Destination Recommendation":

    st.subheader("🌍 Smart Destination Recommendation")

    st.markdown("### 🔍 Similar Destination Recommendation")

    destinations = dest_recommendation.get_destinations()

    selected_destination = st.selectbox(
        "Select Destination",
        destinations
    )

    if st.button("Recommend Similar Destinations"):

        result = dest_recommendation.recommend_destination(
            selected_destination
        )

        st.dataframe(
            result,
            use_container_width=True
        )

    st.markdown("---")


    st.markdown("### 🎯 Recommend By Preferences")

    category = st.selectbox(
        "Category",
        dest_recommendation.get_categories()
    )

    budget = st.selectbox(
        "Budget Level",
        dest_recommendation.get_budget_levels()
    )

    climate = st.selectbox(
        "Climate",
        dest_recommendation.get_climates()
    )

    season = st.selectbox(
        "Best Season",
        dest_recommendation.get_seasons()
    )

    adventure = st.slider(
        "Adventure",
        0,
        1,
        1
    )

    nightlife = st.slider(
        "Nightlife",
        0,
        1,
        0
    )

    family = st.slider(
        "Family Friendly",
        0,
        1,
        1
    )

    trekking = st.slider(
        "Trekking",
        0,
        1,
        0
    )

    beach = st.slider(
        "Beach Activities",
        0,
        1,
        0
    )

    if st.button("Recommend Destinations"):

        result = dest_recommendation.recommend_by_preferences(
            category,
            budget,
            climate,
            season,
            adventure,
            nightlife,
            family,
            trekking,
            beach
        )

        st.dataframe(
            result,
            use_container_width=True
        )