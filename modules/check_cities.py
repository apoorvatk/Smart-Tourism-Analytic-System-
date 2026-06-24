import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "tourism.csv")

df = pd.read_csv(csv_path)

print("Total NaN values:", df.isnull().sum().sum())
print("Shape:", df.shape)