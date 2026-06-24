import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "hotels.csv")

df = pd.read_csv(
    csv_path,
    encoding="latin1",
    low_memory=False
)

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Keep only 1 hotel per city
df = df.groupby("cityName").head(1)

# Keep only columns actually used by the recommender
df = df[
    [
        "HotelName",
        "cityName",
        "HotelRating",
        "HotelFacilities",
        "Description"
    ]
]

output_path = os.path.join(BASE_DIR, "hotels_small.csv")

df.to_csv(
    output_path,
    index=False
)

print("Done!")
print("Rows:", len(df))
print("Columns:", len(df.columns))