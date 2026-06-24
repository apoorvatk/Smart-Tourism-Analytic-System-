import pandas as pd
import os
import streamlit as st

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# LOAD DATA
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_NAME = "tourism.csv"

csv_path = os.path.join(
    BASE_DIR,
    CSV_NAME
)


@st.cache_data
def load_data():

    df = pd.read_csv(csv_path)

    df.columns = df.columns.str.strip()

    return df


df = load_data()


# =========================================================
# FEATURES
# =========================================================

features = [

    "category",
    "budget_level",
    "climate",
    "best_season",

    "adventure",
    "nightlife",
    "family_friendly",
    "trekking",
    "beach_activities",

    "cultural_sites",
    "wildlife",
    "shopping",

    "popularity_score",
    "safety_score",
    "avg_cost_index",
    "rating"
]


categorical_cols = [

    "category",
    "budget_level",
    "climate",
    "best_season"
]


numeric_cols = [

    "adventure",
    "nightlife",
    "family_friendly",
    "trekking",
    "beach_activities",

    "cultural_sites",
    "wildlife",
    "shopping",

    "popularity_score",
    "safety_score",
    "avg_cost_index",
    "rating"
]


# =========================================================
# CLEAN DATA
# =========================================================

for col in categorical_cols:
    df[col] = df[col].fillna("Unknown")

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

    df[col] = df[col].fillna(
        df[col].median()
    )


# =========================================================
# ENCODING
# =========================================================

encoders = {}

df_encoded = df.copy()

for col in categorical_cols:

    le = LabelEncoder()

    df_encoded[col] = le.fit_transform(
        df_encoded[col].astype(str)
    )

    encoders[col] = le


# =========================================================
# SCALING
# =========================================================

scaler = StandardScaler()

feature_matrix = scaler.fit_transform(
    df_encoded[features]
)

similarity_matrix = cosine_similarity(
    feature_matrix
)


# =========================================================
# SIMILAR DESTINATION RECOMMENDATION
# =========================================================
# =========================================================
# SIMILAR DESTINATION RECOMMENDATION
# =========================================================

def recommend_destination(
    city_name,
    top_n=30
):

    city_name = str(
        city_name
    ).strip().lower()

    names = df[
        "name"
    ].astype(str).str.lower()

    matches = df[
        names.str.contains(
            city_name,
            na=False
        )
    ]

    if matches.empty:

        result = df.sort_values(
            by="rating",
            ascending=False
        )

        if top_n is not None:
            result = result.head(top_n)

        return result[
            [
                "name",
                "country",
                "category",
                "rating"
            ]
        ]

    idx = matches.index[0]

    scores = list(
        enumerate(
            similarity_matrix[idx]
        )
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    result_idx = []

    for i, score in scores:

        if i != idx:
            result_idx.append(i)

    if top_n is not None:
        result_idx = result_idx[:top_n]

    return df.iloc[
        result_idx
    ][
        [
            "name",
            "country",
            "category",
            "rating"
        ]
    ]
# =========================================================
# PREFERENCE BASED RECOMMENDATION
# =========================================================

# =========================================================
# PREFERENCE BASED RECOMMENDATION
# =========================================================

def recommend_by_preferences(

    category,
    budget_level,
    climate,
    best_season,

    adventure,
    nightlife,
    family_friendly,
    trekking,
    beach_activities,

    top_n=30

):

    def encode(col, val):

        if val not in encoders[col].classes_:
            return 0

        return encoders[col].transform(
            [val]
        )[0]

    user = pd.DataFrame([{

        "category":
            encode(
                "category",
                category
            ),

        "budget_level":
            encode(
                "budget_level",
                budget_level
            ),

        "climate":
            encode(
                "climate",
                climate
            ),

        "best_season":
            encode(
                "best_season",
                best_season
            ),

        "adventure":
            adventure,

        "nightlife":
            nightlife,

        "family_friendly":
            family_friendly,

        "trekking":
            trekking,

        "beach_activities":
            beach_activities,

        "cultural_sites":
            0,

        "wildlife":
            0,

        "shopping":
            0,

        "popularity_score":
            50,

        "safety_score":
            50,

        "avg_cost_index":
            50,

        "rating":
            4.0
    }])

    user_scaled = scaler.transform(
        user
    )

    scores = cosine_similarity(
        user_scaled,
        feature_matrix
    )[0]

    top_idx = scores.argsort()[::-1]

    if top_n is not None:
        top_idx = top_idx[:top_n]

    return df.iloc[
        top_idx
    ][
        [
            "name",
            "country",
            "category",
            "budget_level",
            "rating"
        ]
    ]

# =========================================================
# DROPDOWN HELPERS
# =========================================================

def get_destinations():

    return sorted(
        df["name"]
        .dropna()
        .unique()
        .tolist()
    )


def get_categories():

    return sorted(
        df["category"]
        .dropna()
        .unique()
        .tolist()
    )


def get_budget_levels():

    return sorted(
        df["budget_level"]
        .dropna()
        .unique()
        .tolist()
    )


def get_climates():

    return sorted(
        df["climate"]
        .dropna()
        .unique()
        .tolist()
    )


def get_seasons():

    return sorted(
        df["best_season"]
        .dropna()
        .unique()
        .tolist()
    )