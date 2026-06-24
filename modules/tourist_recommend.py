
import pandas as pd
import os
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================================================
# FILE PATH
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(
    BASE_DIR,
    "cleaned_data_India.csv"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        csv_path,
        low_memory=False
    )

    df = df[
        [
            "name",
            "city",
            "country",
            "state",
            "main_category",
            "broader_category",
            "rating",
            "reviews",
            "Weighted_Score"
        ]
    ]

    df = df.dropna(
        subset=[
            "name",
            "city",
            "main_category",
            "broader_category"
        ]
    )

    df["combined_features"] = (

        df["main_category"].astype(str)
        + " "
        + df["broader_category"].astype(str)

    )

    return df

# =========================================================
# BUILD MODEL
# =========================================================

@st.cache_resource
def build_model():

    df = load_data()

    tfidf = TfidfVectorizer()

    feature_matrix = tfidf.fit_transform(
        df["combined_features"]
    )

    similarity_matrix = cosine_similarity(
        feature_matrix
    )

    return df, similarity_matrix

# =========================================================
# INIT
# =========================================================

def init():

    return build_model()

# =========================================================
# RECOMMEND BY CITY
# =========================================================

def recommend_by_city(
    city,
    top_n=None
):

    df, _ = init()

    city_places = df[
        df["city"]
        .str.lower()
        .str.contains(
            city.lower(),
            na=False
        )
    ]

    if city_places.empty:
        return pd.DataFrame()

    result = city_places.sort_values(
        by="Weighted_Score",
        ascending=False
    )[
        [
            "name",
            "main_category",
            "rating",
            "reviews"
        ]
    ]

    if top_n is not None:
        result = result.head(top_n)

    return result

# =========================================================
# RECOMMEND BY CITY + CATEGORY
# =========================================================

def recommend_by_city_category(
    city,
    category,
    top_n=None
):

    df, _ = init()

    results = df[
        (
            df["city"]
            .str.lower()
            .str.contains(
                city.lower(),
                na=False
            )
        )
        &
        (
            df["broader_category"]
            .str.lower()
            ==
            category.lower()
        )
    ]

    if results.empty:
        return pd.DataFrame()

    result = results.sort_values(
        by="Weighted_Score",
        ascending=False
    )[
        [
            "name",
            "rating",
            "reviews"
        ]
    ]

    if top_n is not None:
        result = result.head(top_n)

    return result

# =========================================================
# SIMILAR ATTRACTIONS
# =========================================================

def recommend_similar_attraction(
    attraction_name,
    top_n=None
):

    df, similarity_matrix = init()

    match = df[
        df["name"]
        .str.lower()
        ==
        attraction_name.lower()
    ]

    if match.empty:
        return pd.DataFrame()

    idx = match.index[0]

    pos = df.index.get_loc(idx)

    scores = list(
        enumerate(
            similarity_matrix[pos]
        )
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    if top_n is None:

        attraction_indices = [
            i[0]
            for i in scores[1:]
        ]

    else:

        attraction_indices = [
            i[0]
            for i in scores[1:top_n + 1]
        ]

    return df.iloc[
        attraction_indices
    ][
        [
            "name",
            "city",
            "broader_category",
            "rating"
        ]
    ]

# =========================================================
# HELPERS FOR STREAMLIT
# =========================================================

def get_cities():

    df = load_data()

    return sorted(
        df["city"]
        .dropna()
        .unique()
        .tolist()
    )

def get_categories():

    df = load_data()

    return sorted(
        df["broader_category"]
        .dropna()
        .unique()
        .tolist()
    )

def get_attractions():

    df = load_data()

    return sorted(
        df["name"]
        .dropna()
        .unique()
        .tolist()
    )