import pandas as pd
import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "hotels.csv")


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        csv_path,
        encoding="latin1",
        low_memory=False
    )

    df.columns = df.columns.str.strip()

    # Reduce dataset for performance
    if "cityName" in df.columns:
        df = df.groupby("cityName").head(10)

    df = df.dropna(
        subset=[
            "HotelName",
            "cityName",
            "HotelRating"
        ]
    )

    if "Description" not in df.columns:
        df["Description"] = "No Description"

    if "HotelFacilities" not in df.columns:
        df["HotelFacilities"] = "No Facilities"

    df["Description"] = df["Description"].fillna("No Description")
    df["HotelFacilities"] = df["HotelFacilities"].fillna("No Facilities")

    df["combined_features"] = (
        (df["HotelName"].astype(str) + " ") * 2
        + df["cityName"].astype(str) + " "
        + df["HotelRating"].astype(str) + " "
        + df["HotelFacilities"].astype(str) + " "
        + df["Description"].astype(str)
    )

    return df


# =========================================================
# BUILD MODEL
# =========================================================

@st.cache_resource
def build_model():

    df = load_data()

    tfidf = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = tfidf.fit_transform(
        df["combined_features"]
    )

    return df, tfidf, tfidf_matrix


# =========================================================
# GLOBAL INIT
# =========================================================

def init():

    df, tfidf, tfidf_matrix = build_model()

    return df, tfidf, tfidf_matrix


# =========================================================
# SIMILAR HOTEL RECOMMENDATION
# =========================================================

def recommend_hotel(hotel_name, top_n=10):

    df, tfidf, tfidf_matrix = init()

    if df.empty:
        return pd.DataFrame()

    hotel_name = hotel_name.strip().lower()

    match = df[
        df["HotelName"].str.lower() == hotel_name
    ]

    if match.empty:
        return pd.DataFrame()

    idx = match.index[0]

    pos = df.index.get_loc(idx)

    query_vec = tfidf_matrix[pos]

    scores = cosine_similarity(
        query_vec,
        tfidf_matrix
    ).flatten()

    top_indices = scores.argsort()[-top_n-1:][::-1]

    top_indices = [
        i for i in top_indices
        if i != pos
    ]

    return df.iloc[top_indices][
        [
            "HotelName",
            "cityName",
            "HotelRating",
            "HotelFacilities"
        ]
    ]


# =========================================================
# CITY WISE HOTELS
# =========================================================
def recommend_hotels_by_city(city_name, top_n=20):

    df, _, _ = init()

    if df.empty:
        return pd.DataFrame()

    city_name = city_name.strip().lower()

    filtered = df[
        df["cityName"]
        .str.lower()
        .str.contains(city_name, na=False)
    ]

    if filtered.empty:
        return pd.DataFrame()

    return filtered.sort_values(
        by="HotelRating",
        ascending=False
    ).head(top_n)[
        [
            "HotelName",
            "cityName",
            "HotelRating",
            "HotelFacilities"
        ]
    ]
# =========================================================
# HOTEL LIST FOR DROPDOWN
# =========================================================

def get_hotels():

    df, _, _ = init()

    if df.empty:
        return []

    return sorted(
        df["HotelName"]
        .dropna()
        .unique()
        .tolist()
    )


# =========================================================
# CITY LIST FOR DROPDOWN
# =========================================================

def get_cities():

    df, _, _ = init()

    if df.empty:
        return []

    return sorted(
        df["cityName"]
        .dropna()
        .unique()
        .tolist()
    )